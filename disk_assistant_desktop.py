"""Desktop launcher for the read-only scanner."""
from datetime import datetime
from pathlib import Path
import queue
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import webbrowser

from disk_assistant import scan, render_report, human_size


def main():
    app = tk.Tk()
    app.title('磁盘空间分析助手 v0.1.0')
    app.geometry('640x350')
    path = tk.StringVar()
    status = tk.StringVar(value='选择盘符或文件夹，完成后保存 HTML 报告。')
    depth = tk.StringVar(value='')
    seconds = tk.StringVar(value='')
    events = queue.Queue()
    report = [None]
    frame = ttk.Frame(app, padding=24)
    frame.pack(fill='both', expand=True)
    ttk.Label(frame, text='磁盘空间分析助手', font=('Microsoft YaHei', 18)).pack(anchor='w')
    ttk.Label(frame, text='只读扫描 · 本地报告 · 默认不限深度 · 当前建议为规则分析').pack(anchor='w', pady=8)
    row = ttk.Frame(frame)
    row.pack(fill='x', pady=8)
    ttk.Entry(row, textvariable=path).pack(side='left', fill='x', expand=True)
    def choose():
        value = filedialog.askdirectory()
        if value:
            path.set(value)
    ttk.Button(row, text='选择目录', command=choose).pack(side='left', padx=8)
    limits = ttk.Frame(frame)
    limits.pack(fill='x', pady=8)
    ttk.Label(limits, text='最大深度（空=不限）').pack(side='left')
    ttk.Entry(limits, textvariable=depth, width=7).pack(side='left', padx=8)
    ttk.Label(limits, text='最长秒数（空=不限）').pack(side='left')
    ttk.Entry(limits, textvariable=seconds, width=7).pack(side='left', padx=8)
    ttk.Label(frame, textvariable=status, wraplength=580).pack(anchor='w', pady=16)
    def worker(target, output, depth_limit, time_limit):
        try:
            result = scan(target, max_depth=depth_limit, max_seconds=time_limit,
                          progress=lambda dirs, files: events.put(('progress', f'已扫描 {dirs:,} 个目录，{files:,} 个文件')))
            with output.open('x', encoding='utf-8') as stream:
                stream.write(render_report(result))
            events.put(('done', (output, result)))
        except Exception as exc:
            events.put(('error', str(exc)))
    def start():
        try:
            d = int(depth.get()) if depth.get().strip() else None
            s = float(seconds.get()) if seconds.get().strip() else None
            if (d is not None and d < 0) or (s is not None and s <= 0):
                raise ValueError()
            if not Path(path.get()).is_dir():
                raise ValueError()
        except ValueError:
            messagebox.showerror('请检查输入', '选择有效目录；深度需非负，秒数需大于零。')
            return
        name = filedialog.asksaveasfilename(defaultextension='.html',
            initialfile=f'disk-report-{datetime.now():%Y%m%d-%H%M%S}.html',
            filetypes=[('HTML 报告', '*.html')])
        if not name:
            return
        output = Path(name)
        if output.exists():
            messagebox.showerror('请选择新文件名', '为保护已有文件，不覆盖现有报告。')
            return
        run_button.configure(state='disabled')
        open_button.configure(state='disabled')
        status.set('正在扫描…深层或较大的目录可能需要一些时间。')
        threading.Thread(target=worker, args=(path.get(), output, d, s), daemon=True).start()
    run_button = ttk.Button(frame, text='开始扫描并保存报告', command=start)
    run_button.pack(side='left')
    open_button = ttk.Button(frame, text='打开报告', state='disabled',
        command=lambda: webbrowser.open(report[0].resolve().as_uri()))
    open_button.pack(side='left', padx=12)
    def poll():
        try:
            while True:
                kind, value = events.get_nowait()
                if kind == 'progress':
                    status.set(value)
                elif kind == 'done':
                    output, result = value
                    report[0] = output
                    status.set(f"已完成：{human_size(result['bytes'])}，{result['files']:,} 个文件；状态 {result['status']}；读取错误 {result['errors']} 项。报告：{output}")
                    run_button.configure(state='normal')
                    open_button.configure(state='normal')
                else:
                    status.set('扫描失败：' + value)
                    run_button.configure(state='normal')
        except queue.Empty:
            pass
        app.after(200, poll)
    poll()
    app.mainloop()


if __name__ == '__main__':
    main()
