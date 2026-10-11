"""Disk Space Assistant: integrated desktop inventory and AI analysis."""
from datetime import datetime
import json
import os
import shutil
import tempfile
from pathlib import Path
import queue
import sys
import threading
import time
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from disk_assistant import scan, render_report, human_size
from cloud_analysis import load_report, prepare_items, analyze_selected, validate_settings
from file_records import file_records
from report_open import open_report
from cleanup_actions import recycle
from scan_index import directory_page
from disk_assistant import cleanup_assessment
from desktop_theme import apply_theme, scope_message, drive_colors, BG, INK, MUTED, NAVY


def main():
    app = tk.Tk()
    if '--self-test' in sys.argv:
        app.withdraw()
    app.title('磁盘空间分析助手 v0.6.0')
    app.geometry('1320x860')
    app.minsize(1100, 740)
    app.configure(background=BG)
    style = ttk.Style(app)
    apply_theme(style)
    state = {'result': None, 'records': {}, 'busy': False, 'started': 0, 'completed': 0,
             'total': 0, 'phase': '', 'cancel': threading.Event(), 'config': {},
             'sort_column': 'size', 'sort_reverse': True}
    state.update(browse=None, browse_page=0, browser_items={}, selected_directory=None, browse_sort='bytes', browse_reverse=True)
    events = queue.Queue()
    sidebar = tk.Frame(app, background=NAVY, width=190)
    sidebar.pack(side='left', fill='y')
    sidebar.pack_propagate(False)
    tk.Label(sidebar, text='SPACE\nASSISTANT', background=NAVY, foreground='white', font=('Segoe UI', 19, 'bold'), justify='left').pack(anchor='w', padx=22, pady=(30, 8))
    tk.Label(sidebar, text='磁盘空间分析助手', background=NAVY, foreground='#91a6c6', font=('Microsoft YaHei', 10)).pack(anchor='w', padx=22, pady=(0, 24))
    navigation_area = tk.Frame(sidebar, background=NAVY)
    navigation_area.pack(fill='x', padx=12)
    tk.Label(sidebar, text='v0.6.0\n扫描只读 · 清理需确认', background=NAVY, foreground='#91a6c6', font=('Microsoft YaHei', 9), justify='left').pack(side='bottom', anchor='w', padx=22, pady=24)
    root = ttk.Frame(app, padding=24)
    root.pack(side='left', fill='both', expand=True)
    ttk.Label(root, text='空间总览', font=('Microsoft YaHei', 23, 'bold')).pack(anchor='w')
    scope_text = tk.StringVar(value='选择整盘或文件夹开始。先查看目录总量，再检查具体文件。')
    ttk.Label(root, textvariable=scope_text, style='Scope.TLabel', wraplength=970).pack(fill='x', pady=(12, 14))
    metrics = ttk.Frame(root)
    metrics.pack(fill='x', pady=(0, 12))
    metric_values = [tk.StringVar(value='—') for _ in range(4)]
    for i, label in enumerate(['已统计逻辑占用', '已扫描文件', '读取错误', 'AI 分析覆盖']):
        metrics.columnconfigure(i, weight=1)
        card = ttk.Frame(metrics, style='Card.TFrame', padding=(16, 12))
        card.grid(row=0, column=i, sticky='nsew', padx=(0, 10 if i < 3 else 0))
        ttk.Label(card, text=label, style='Card.TLabel').pack(anchor='w')
        ttk.Label(card, textvariable=metric_values[i], style='Metric.TLabel').pack(anchor='w', pady=(5, 0))
    summary = tk.StringVar(value='扫描目录，或导入已有 HTML 报告；文件和 AI 解释会显示在同一处。')
    ttk.Label(root, textvariable=summary, wraplength=970, style='Muted.TLabel').pack(anchor='w', pady=(0, 8))
    toolbar = ttk.Frame(root)
    toolbar.pack(fill='x')
    scan_limits = ttk.Frame(root)
    scan_limits.pack(fill='x', pady=8)
    max_depth, max_seconds = tk.StringVar(), tk.StringVar()
    for label, variable in [('最大扫描深度（空=不限）', max_depth), ('最长秒数（空=不限）', max_seconds)]:
        ttk.Label(scan_limits, text=label).pack(side='left', padx=(0, 8))
        ttk.Entry(scan_limits, textvariable=variable, width=8).pack(side='left', padx=(0, 16))
    status = tk.StringVar(value='就绪 · 扫描只读 · 移入回收站需逐项确认')
    progress = ttk.Progressbar(root, mode='determinate', maximum=100)
    progress.pack(fill='x', pady=(12, 4))
    ttk.Label(root, textvariable=status, wraplength=1080).pack(anchor='w')
    filters = ttk.Frame(root)
    filters.pack(fill='x', pady=12)
    query = tk.StringVar()
    scope = tk.StringVar(value='全部')
    ttk.Label(filters, text='搜索文件 / 软件 / 路径').pack(side='left')
    ttk.Entry(filters, textvariable=query, width=35).pack(side='left', padx=10)
    combo = ttk.Combobox(filters, textvariable=scope, values=['全部', '未分析', '已分析'], state='readonly', width=12)
    combo.pack(side='left')
    ttk.Label(filters, text='Ctrl / Shift 多选；每轮最多 20 项，分批处理，可继续下一轮').pack(side='left', padx=12)
    panes = ttk.Panedwindow(root, orient='horizontal')
    panes.pack(fill='both', expand=True)
    left, right = ttk.Frame(panes), ttk.Frame(panes, padding=16, style='Card.TFrame')
    panes.add(left, weight=3)
    panes.add(right, weight=2)
    notebook = ttk.Notebook(left)
    notebook.pack(fill='both', expand=True)
    candidate_tab, browser_tab = ttk.Frame(notebook), ttk.Frame(notebook)
    notebook.add(browser_tab, text='目录层级与空间图')
    notebook.add(candidate_tab, text='重点清单与 AI')
    tree = ttk.Treeview(candidate_tab, columns=('name', 'size', 'status', 'rule'), show='headings', selectmode='extended')
    for column, label, width in [('name', '文件 / AI 名称', 250), ('size', '大小', 90), ('status', 'AI 状态', 80), ('rule', '本地规则提示', 160)]:
        tree.heading(column, text=label, command=lambda c=column: sort_by(c))
        tree.column(column, width=width, minwidth=70)
    scroll = ttk.Scrollbar(candidate_tab, orient='vertical', command=tree.yview)
    tree.configure(yscrollcommand=scroll.set)
    tree.pack(side='left', fill='both', expand=True)
    scroll.pack(side='right', fill='y')
    title = tk.StringVar(value='选中一个文件查看用途与影响')
    ttk.Label(right, textvariable=title, style='Card.TLabel', font=('Microsoft YaHei', 14, 'bold'), wraplength=330).pack(anchor='w', pady=(0, 12))
    detail = tk.Text(right, wrap='word', relief='flat', borderwidth=0, background='white', foreground=INK, selectbackground='#dbeafe', font=('Microsoft YaHei', 10), padx=8, pady=8, spacing3=8)
    detail.pack(fill='both', expand=True)
    controls = []
    navigation = ttk.Frame(browser_tab)
    navigation.pack(fill='x', pady=4)
    location = tk.StringVar(value='先扫描或导入报告')
    ttk.Label(browser_tab, textvariable=location, wraplength=580).pack(anchor='w', pady=4)
    canvas = tk.Canvas(browser_tab, height=210, background='#edf2fa', highlightthickness=0)
    canvas.pack(fill='x', pady=8)
    browser_tree = ttk.Treeview(browser_tab, columns=('name', 'bytes', 'kind'), show='headings', height=8)
    for col, text in [('name', '该层目录 / 文件（双击进入）'), ('bytes', '逻辑大小'), ('kind', '类型')]:
        browser_tree.heading(col, text=text, command=lambda c=col: sort_browser(c))
        browser_tree.column(col, width=260 if col == 'name' else 100)
    browse_scroll = ttk.Scrollbar(browser_tab, orient='vertical', command=browser_tree.yview)
    browser_tree.configure(yscrollcommand=browse_scroll.set)
    browse_scroll.pack(side='right', fill='y')
    browser_tree.pack(fill='both', expand=True)
    browse_info = tk.StringVar()
    ttk.Label(browser_tab, textvariable=browse_info, wraplength=580).pack(anchor='w', pady=6)

    def browse(path=None, delta=0):
        result = state['result']
        if not result:
            return
        current = path or state['browse'] or result['root']
        state['browse_page'] = 0 if path else max(0, state['browse_page'] + delta)
        state['browse'] = current
        rows = []
        index_path = result.get('index_path')
        if index_path and Path(index_path).is_file():
            total, rows, children = directory_page(index_path, current, state['browse_page'], sort=state['browse_sort'], descending=state['browse_reverse'])
            max_page = max(0, (total - 1) // 100)
            if state['browse_page'] > max_page:
                state['browse_page'] = max_page
                total, rows, children = directory_page(index_path, current, max_page, sort=state['browse_sort'], descending=state['browse_reverse'])
            note = f"该层已索引文件 {total} 个；第 {state['browse_page'] + 1} / {max_page + 1} 页，每页 100 项。"
        else:
            children = [(n['path'], n['bytes']) for n in result.get('directory_map', []) if n.get('parent') == current]
            all_rows = [n for n in file_records(result) if str(Path(n['path']).parent) == current]
            rows = all_rows[state['browse_page'] * 100:(state['browse_page'] + 1) * 100]
            note = '旧报告只有部分明细，不是完整目录。重新扫描可建立完整文件索引。'
        try:
            depth = len(Path(current).relative_to(Path(result['root'])).parts)
        except ValueError:
            depth = 0
        location.set(f'{current} · 第 {depth} 层（扫描根目录为第 0 层）')
        children.sort(key=(lambda n: n[1]) if state['browse_sort'] == 'bytes' else (lambda n: Path(n[0]).name.casefold()), reverse=state['browse_reverse'])
        browser_tree.delete(*browser_tree.get_children())
        state['browser_items'] = {}
        for p, size in children:
            state['browser_items'][p] = {'path': p, 'bytes': size, 'directory': True}
            browser_tree.insert('', 'end', iid=p, values=(Path(p).name or p, human_size(size), '目录'))
        for item in rows:
            p = item['path']
            state['browser_items'][p] = item
            browser_tree.insert('', 'end', iid=p, values=(Path(p).name, human_size(item['bytes']), '文件'))
        browse_info.set(note + ' 大小仍是扫描快照；跳过/未扫描的部分不会计入。')
        canvas.delete('all')
        colors = drive_colors(current)
        drive = Path(current).drive.upper()
        offset = 0
        tiles = sorted(children, key=lambda n: n[1], reverse=True)[:6]
        width = max(canvas.winfo_width(), 400)
        columns = 3 if width >= 620 else 2
        canvas.configure(height=(len(tiles) + columns - 1) // columns * 49 + 28)
        current_total = next((n['bytes'] for n in result.get('directory_map', []) if n['path'] == current), sum(n[1] for n in children))
        title.set(Path(current).name or current)
        set_detail(f'目录位置\n{current}\n\n已统计逻辑占用\n{human_size(current_total)}\n\n当前层级\n第 {depth} 层，扫描根目录为第 0 层\n\n浏览说明\n{note}\n\n目录总量包含子目录和直接文件。查看大目录中的组成后，再决定具体文件；不能把目录总量当作可释放空间。')
        for i, (p, size) in enumerate(tiles):
            x, y = (i % columns) * width / columns, (i // columns) * 49
            ratio = size / max(current_total, 1)
            rect = canvas.create_rectangle(x + 2, y + 28, x + 2 + max(2, (width / columns - 10) * ratio), y + 42, fill=colors[(i + offset) % len(colors)], outline='')
            text = canvas.create_text(x + 6, y + 12, text=f'{Path(p).name[:9]} · {human_size(size)} ({ratio:.0%})', anchor='w', fill='#243851', font=('Microsoft YaHei', 9))
            canvas.tag_bind(rect, '<Button-1>', lambda event, target=p: browse(target))
            canvas.tag_bind(text, '<Button-1>', lambda event, target=p: browse(target))
        if not tiles:
            canvas.create_text(15, 30, text='此层无已扫描子目录；文件见下方。', anchor='w', fill='#52647c')
        canvas.create_text(8, (len(tiles) + columns - 1) // columns * 49 + 18, text=f'{drive or "当前卷"} · 前 6 个目录占比，点击下钻；完整目录见下表。', anchor='w', fill=colors[offset], font=('Microsoft YaHei', 9))

    def parent_directory():
        if state['result'] and state['browse'] != state['result']['root']:
            browse(str(Path(state['browse']).parent))
    def sort_browser(column):
        sort = 'bytes' if column == 'bytes' else 'name'
        state['browse_reverse'] = not state['browse_reverse'] if sort == state['browse_sort'] else sort == 'bytes'
        state['browse_sort'] = sort
        state['browse_page'] = 0
        browse()
    for label, cmd in [('上一级', parent_directory), ('根目录', lambda: browse(state['result']['root']) if state['result'] else None),
                       ('前页', lambda: browse(delta=-1)), ('后页', lambda: browse(delta=1))]:
        ttk.Button(navigation, text=label, command=cmd).pack(side='left', padx=3)

    def browse_open(event=None):
        chosen = browser_tree.selection()
        if not chosen:
            return
        item = state['browser_items'][chosen[0]]
        if item.get('directory'):
            browse(item['path'])
        else:
            result = state['result']
            if item['path'] not in {n['path'] for n in result['largest_files']}:
                result['largest_files'].append(dict(item, **cleanup_assessment(item['path'])))
            notebook.select(candidate_tab)
            query.set('')
            scope.set('全部')
            refresh()
            tree.selection_set(item['path'])
            tree.see(item['path'])
            show_item()
    browser_tree.bind('<Double-1>', browse_open)

    def set_detail(text):
        detail.configure(state='normal')
        detail.delete('1.0', 'end')
        detail.insert('1.0', text)
        detail.configure(state='disabled')

    def show_item(event=None):
        selection = tree.selection()
        if not selection:
            return
        item = state['records'][selection[0]]
        ai = item.get('ai')
        name = ai.get('name', '') if ai else Path(item['path']).name
        title.set(name)
        text = f"路径：{item['path']}\n大小：{human_size(item.get('bytes', 0))}\n\n本地规则：{item['label']}\n{item['reason']}\n{item['impact']}\n\n"
        if ai:
            text += '\n\n'.join([f"是什么：{ai['description']}", f"属于哪个软件：{ai['owner']}",
                f"AI 建议（非删除许可）：{ai['decision']}", f"处理影响：{ai['impact']}",
                f"推荐方式：{ai['method']}", f"证据状态：{ai['evidence_status']}"])
            text += '\n\n来源：\n' + '\n'.join(s['url'] for s in ai.get('sources', []))
            text += '\n\nAI 与规则不一致时先保留并核实；未检测备份、文件是否在使用或可恢复性。'
        else:
            text += '尚未请求 AI，不是 AI 不认识该文件。选中后点击“分析选中文件”。'
        set_detail(text)

    def refresh():
        old = set(tree.selection())
        tree.delete(*tree.get_children())
        result = state['result']
        if not result:
            return
        rows = file_records(result)
        keys = {'name': lambda n: (n.get('ai', {}).get('name') or Path(n['path']).name).casefold(),
                'size': lambda n: n.get('bytes', 0), 'status': lambda n: n['analysis_status'],
                'rule': lambda n: n['label']}
        rows.sort(key=keys[state['sort_column']], reverse=state['sort_reverse'])
        state['records'] = {item['path']: item for item in rows}
        q = query.get().lower()
        for item in rows:
            ai = item.get('ai', {})
            if scope.get() != '全部' and item['analysis_status'] != scope.get():
                continue
            if q not in (item['path'] + ai.get('name', '') + ai.get('owner', '')).lower():
                continue
            tree.insert('', 'end', iid=item['path'], values=(ai.get('name') or Path(item['path']).name,
                human_size(item.get('bytes', 0)), item['analysis_status'], item['label']))
        selected = [p for p in old if tree.exists(p)]
        visible = tree.get_children()
        if selected:
            tree.selection_set(selected)
        elif visible:
            tree.selection_set(visible[0])
        analyzed = sum('ai' in n for n in rows)
        scope_text.set(scope_message(result['root']))
        for variable, value in zip(metric_values, [human_size(result['bytes']), f"{result['files']:,}", str(result['errors']), f'{analyzed} / {len(rows)}']):
            variable.set(value)
        summary.set(f"{result['root']} · 已统计 {human_size(result['bytes'])} · 状态 {result['status']} · 当前重点清单 {len(rows)} 项 · AI 已分析 {analyzed} / {len(rows)} 项\n完整文件明细请到“目录层级与空间图”；旧报告缺失的明细需要重新扫描。")
        show_item()

    def sort_by(column):
        state['sort_reverse'] = not state['sort_reverse'] if column == state['sort_column'] else column == 'size'
        state['sort_column'] = column
        refresh()

    def busy(phase, total=0):
        state.update(busy=True, phase=phase, started=time.monotonic(), completed=0, total=total)
        state['cancel'].clear()
        for button in controls:
            button.configure(state='disabled')
        progress.configure(mode='indeterminate')
        progress.start(12)
        cancel_button.configure(state='normal' if phase == 'AI' else 'disabled')

    def finish():
        state['busy'] = False
        progress.stop()
        progress.configure(mode='determinate', maximum=100)
        progress['value'] = state['completed'] / state['total'] * 100 if state['total'] else 0
        for button in controls:
            button.configure(state='normal')
        cancel_button.configure(state='disabled')

    def import_existing():
        filename = filedialog.askopenfilename(filetypes=[('扫描或 AI 报告', '*.html')])
        if not filename:
            return
        busy('导入')
        def work():
            try:
                events.put(('loaded', load_report(filename)))
            except Exception as exc:
                events.put(('error', str(exc)))
        threading.Thread(target=work, daemon=True).start()

    def start_scan(target=None):
        try:
            depth_limit = int(max_depth.get()) if max_depth.get().strip() else None
            time_limit = float(max_seconds.get()) if max_seconds.get().strip() else None
            if (depth_limit is not None and depth_limit < 0) or (time_limit is not None and time_limit <= 0):
                raise ValueError()
        except ValueError:
            messagebox.showerror('扫描限制', '深度填写非负整数，秒数大于 0；留空表示不限。')
            return
        target = target or filedialog.askdirectory(title='选择要分析的盘符或文件夹')
        if not target:
            return
        busy('扫描')
        def work():
            try:
                handle, index_path = tempfile.mkstemp(prefix='disk-assistant-', suffix='.sqlite')
                os.close(handle)
                result = scan(target, top=100, max_depth=depth_limit, max_seconds=time_limit,
                              index_path=index_path,
                              progress=lambda dirs, files: events.put(('scan_progress', (dirs, files))))
                events.put(('loaded', result))
            except Exception as exc:
                events.put(('error', str(exc)))
        threading.Thread(target=work, daemon=True).start()

    def select_unanalyzed():
        ids = [p for p in tree.get_children() if 'ai' not in state['records'][p]][:20]
        tree.selection_set(ids)
        if ids:
            tree.see(ids[0])
        show_item()

    def global_settings(callback=None):
        dialog = tk.Toplevel(app)
        dialog.title('全局 API 设置 · 本次运行内复用')
        dialog.geometry('670x420')
        config = state['config']
        endpoint = tk.StringVar(value=config.get('endpoint', 'https://api.deepseek.com/chat/completions'))
        model = tk.StringVar(value=config.get('model', ''))
        key = tk.StringVar(value=config.get('key', ''))
        mode = tk.StringVar(value=config.get('mode', 'chat'))
        ttk.Label(dialog, text='设置一次后，所有分析批次共用。关闭客户端后密钥清除。', wraplength=620).pack(padx=16, pady=12)
        for label, variable, masked in [('完整 HTTPS API 地址', endpoint, False), ('API 密钥', key, True)]:
            ttk.Label(dialog, text=label).pack(anchor='w', padx=16, pady=4)
            ttk.Entry(dialog, textvariable=variable, show='*' if masked else '').pack(fill='x', padx=16)
        ttk.Label(dialog, text='模型名称（可选择示例或手动填写账户支持的名称）').pack(anchor='w', padx=16, pady=4)
        ttk.Combobox(dialog, textvariable=model, values=['deepseek-chat', 'deepseek-reasoner', 'deepseek-flash', 'deepseek-v4-pro']).pack(fill='x', padx=16)
        ttk.Label(dialog, text='示例列表不代表你的账户可用模型。Chat 仅推测；Search 需 Responses 联网工具。').pack(anchor='w', padx=16, pady=6)
        ttk.Combobox(dialog, textvariable=mode, values=['chat', 'search'], state='readonly').pack(anchor='w', padx=16)
        def save():
            if not all(v.get().strip() for v in (endpoint, model, key)):
                messagebox.showerror('配置不完整', '填写地址、模型和密钥。', parent=dialog)
                return
            try:
                validate_settings(endpoint.get().strip(), model.get().strip(), key.get().strip(), mode.get())
            except ValueError as exc:
                messagebox.showerror('API 配置需修改', str(exc), parent=dialog)
                return
            state['config'] = dict(endpoint=endpoint.get().strip(), model=model.get().strip(), key=key.get().strip(), mode=mode.get())
            key.set('')
            dialog.destroy()
            status.set('全局 API 配置已在本次运行中保存。')
            if callback:
                callback()
        ttk.Button(dialog, text='应用全局设置', command=save).pack(pady=16)

    def ai_settings():
        selected = [state['records'][p] for p in tree.selection()]
        if not selected or len(selected) > 20:
            messagebox.showinfo('选择文件', '请从清单选择 1–20 项；可点击“选下一批未分析”。')
            return
        if not state['config']:
            global_settings(ai_settings)
            return
        dialog = tk.Toplevel(app)
        dialog.title(f'发送确认 · 分析你选中的 {len(selected)} 项')
        dialog.geometry('740x640')
        config = dict(state['config'])
        ttk.Label(dialog, text=f"使用全局模型：{config['model']} · 模式：{config['mode']}\n修改请使用主窗口的 API 设置。", wraplength=700).pack(anchor='w', padx=16, pady=12)
        ttk.Label(dialog, text='Chat 仅为模型推测；Search 需要支持 Responses 联网工具的服务。\n以下是实际发送摘要；请检查残留的个人信息。可能产生 API/搜索费用，无自动重试。').pack(anchor='w', padx=16)
        _, public = prepare_items({'cleanup_candidates': [], 'largest_files': selected}, len(selected))
        preview = tk.Text(dialog, height=12, wrap='word')
        preview.pack(fill='both', expand=True, padx=16, pady=8)
        preview.insert('1.0', json.dumps(public, ensure_ascii=False, indent=2))
        preview.configure(state='disabled')
        def send():
            values = config['endpoint'], config['model'], config['key'], config['mode']
            dialog.destroy()
            busy('AI', len(selected))
            def work():
                try:
                    done = analyze_selected(state['result'], selected, *values,
                        progress=lambda n, total, stage: events.put(('ai_progress', (n, total, stage))), cancelled=state['cancel'])
                    events.put(('ai_done', done))
                except Exception as exc:
                    events.put(('error', str(exc)))
            threading.Thread(target=work, daemon=True).start()
        ttk.Button(dialog, text=f'确认发送并分析选中的 {len(selected)} 项', command=send).pack(pady=10)

    def recycle_selected():
        selection = tree.selection()
        if not selection:
            return
        if len(selection) != 1:
            messagebox.showinfo('逐项确认', '本版本每次仅允许一个文件，避免误清理整批。')
            return
        item = state['records'][selection[0]]
        if item['level'] == 'keep':
            messagebox.showinfo('建议保留', '此项受保护或用途未知，建议通过所属软件处理。')
            return
        if not messagebox.askyesno('确认移入回收站', f"{item['path']}\n\n逻辑大小：{human_size(item['bytes'])}\n影响：{item['impact']}\n\n确认不再需要这个文件？进入回收站后可能尚未释放磁盘空间。恢复能力未保证。"):
            return
        try:
            recycle(item)
            state['result'].setdefault('cleanup_log', []).append({'path': item['path'], 'action': 'recycle', 'date': datetime.now().isoformat()})
            for field in ('cleanup_candidates', 'largest_files', 'ai_findings'):
                state['result'][field] = [n for n in state['result'].get(field, []) if n['path'] != item['path']]
            refresh()
            status.set('已提交回收站操作。空间统计为扫描快照，请重新扫描；清理记录可随报告导出。')
        except Exception as exc:
            messagebox.showerror('无法移入回收站', str(exc) + '\n不会改为永久删除。')

    def export_report():
        if not state['result']:
            return
        filename = filedialog.asksaveasfilename(defaultextension='.html',
            initialfile=f'disk-report-{datetime.now():%Y%m%d-%H%M%S}.html', filetypes=[('HTML', '*.html')])
        if not filename:
            return
        try:
            with Path(filename).open('x', encoding='utf-8') as stream:
                stream.write(render_report(state['result']))
            if messagebox.askyesno('已导出', '报告已保存。是否用 Edge/Chrome 打开？'):
                open_report(filename)
        except Exception as exc:
            messagebox.showerror('导出或打开失败', str(exc))

    def nav_button(label, command):
        button = tk.Button(navigation_area, text=label, command=command, anchor='w', relief='flat', borderwidth=0, background=NAVY, activebackground='#253c5f', foreground='#e4edf9', activeforeground='white', font=('Microsoft YaHei', 10), padx=14, pady=12, cursor='hand2')
        button.pack(fill='x', pady=2)
        controls.append(button)
    nav_button('空间与目录', lambda: notebook.select(browser_tab))
    nav_button('文件与 AI', lambda: notebook.select(candidate_tab))
    nav_button('API 设置', global_settings)
    nav_button('导入报告', import_existing)
    nav_button('导出报告', export_report)
    drive_var = tk.StringVar(value='C:/')
    drives = ['C:/']
    if os.name == 'nt':
        import ctypes
        mask = ctypes.windll.kernel32.GetLogicalDrives()
        drives = [f'{chr(65+i)}:/' for i in range(26) if mask & (1 << i) and ctypes.windll.kernel32.GetDriveTypeW(os.path.abspath(f'{chr(65+i)}:/')) in (2, 3)] or drives
    ttk.Combobox(navigation_area, textvariable=drive_var, values=drives, state='readonly', width=12).pack(fill='x', padx=10, pady=(24, 6))
    volume_text = tk.StringVar()
    def volume_usage(*args):
        try:
            usage = shutil.disk_usage(drive_var.get())
            volume_text.set(f'整盘当前已用 {human_size(usage.used)}\n可用 {human_size(usage.free)}\n与扫描逻辑总量口径不同')
        except OSError:
            volume_text.set('整盘容量暂不可读取')
    tk.Label(navigation_area, textvariable=volume_text, background=NAVY, foreground='#91a6c6', font=('Microsoft YaHei', 9), justify='left').pack(anchor='w', padx=12, pady=6)
    drive_var.trace_add('write', volume_usage)
    volume_usage()
    nav_button('扫描所选整盘', lambda: start_scan(drive_var.get()))
    nav_button('扫描指定文件夹', start_scan)
    for label, command, button_style in [('选下一批未分析', select_unanalyzed, 'TButton'), ('AI 分析选中项', ai_settings, 'Primary.TButton'), ('移入回收站', recycle_selected, 'Danger.TButton')]:
        button = ttk.Button(toolbar, text=label, command=command, style=button_style)
        button.pack(side='left', padx=(0, 8))
        controls.append(button)
    cancel_button = ttk.Button(toolbar, text='本批返回后停止', state='disabled', command=state['cancel'].set)
    cancel_button.pack(side='left')
    tree.bind('<<TreeviewSelect>>', show_item)
    combo.bind('<<ComboboxSelected>>', lambda e: refresh())
    query.trace_add('write', lambda *a: refresh() if not state['busy'] else None)
    notebook.bind('<<NotebookTabChanged>>', lambda e: browse() if notebook.select() == str(browser_tab) else show_item())

    def poll():
        try:
            while True:
                kind, value = events.get_nowait()
                if kind == 'scan_progress':
                    state['phase'] = f'扫描：{value[0]:,} 目录 / {value[1]:,} 文件'
                elif kind == 'ai_progress':
                    n, total, stage = value
                    state.update(completed=n, total=total, phase='AI：' + stage)
                    progress.stop()
                    progress.configure(mode='determinate', maximum=total)
                    progress['value'] = n
                    refresh()
                elif kind == 'loaded':
                    state['result'] = value
                    finish()
                    refresh()
                    browse(value['root'])
                    status.set('已载入；直接在清单里查看和选择，不需要打开浏览器。')
                elif kind == 'ai_done':
                    state['completed'] = value
                    total = state['total']
                    finish()
                    refresh()
                    status.set(f'本轮已完成 {value} / {total} 项；结果已并入清单。可继续下一批或导出保存。')
                elif kind == 'error':
                    finish()
                    refresh()
                    status.set('操作失败：' + value + ' 已完成的批次保留在清单中，请导出保存。')
                    messagebox.showerror('操作失败', value)
        except queue.Empty:
            pass
        if state['busy']:
            elapsed = int(time.monotonic() - state['started'])
            status.set(f"{state['phase']} · 已等待 {elapsed} 秒 · 已完成 {state['completed']} / {state['total']} 项" +
                       (' · 单次网络等待上限约 120 秒；进度按完整批次计算，不表示模型生成百分比。' if state['total'] else ''))
        app.after(200, poll)

    def close():
        if state['busy'] and not messagebox.askyesno('任务尚未结束', '关闭会丢失未导出的结果，并结束客户端等待；远端请求可能已计费。仍然退出？'):
            return
        state['config'].clear()
        app.destroy()
    app.protocol('WM_DELETE_WINDOW', close)
    poll()
    if '--self-test' in sys.argv:
        if '--load' in sys.argv:
            state['result'] = load_report(sys.argv[sys.argv.index('--load') + 1])
            refresh()
            browse(state['result']['root'])
        app.update()
        app.destroy()
    else:
        app.mainloop()


if __name__ == '__main__':
    main()
