"""Read-only disk space analysis: python disk_assistant.py PATH --report report.html"""

import argparse
from collections import Counter
import heapq
import html
import json
import os
from pathlib import Path
import stat
import sys
import time


def human_size(value):
    for unit in ("B", "KiB", "MiB", "GiB", "TiB"):
        if value < 1024 or unit == "TiB":
            return f"{value:,.1f} {unit}"
        value /= 1024


def advice(path):
    suffix = Path(path).suffix.lower()
    if suffix in {".zip", ".7z", ".rar", ".iso", ".exe", ".msi"}:
        return "安装包或归档候选；先确认是否仍需保留，不能仅凭后缀判定可删。"
    if suffix in {".mp4", ".mkv", ".mov", ".avi"}:
        return "视频候选；检查是否需要保留，可考虑迁移到其他盘。"
    if suffix in {".log", ".tmp"}:
        return "日志或临时文件候选；确认所属程序和是否正在使用。"
    return "用途尚不确定；检查所属软件或内容后再决定。"


def io_path(path):
    """Use Windows extended paths for IO, keep readable paths in reports."""
    if os.name != "nt" or path.startswith("\\\\?\\"):
        return path
    if path.startswith("\\\\"):
        return "\\\\?\\UNC\\" + path[2:]
    return "\\\\?\\" + path


def scan(directory, top=20, progress=None, max_depth=None, max_seconds=None, max_files=None):
    if top < 1 or (max_depth is not None and max_depth < 0):
        raise ValueError("top 必须大于 0，max_depth 必须非负")
    if any(value is not None and value <= 0 for value in (max_seconds, max_files)):
        raise ValueError("时间和文件数量上限必须大于 0")
    root = os.path.abspath(os.fspath(directory))
    root_stat = os.lstat(io_path(root))
    if stat.S_ISLNK(root_stat.st_mode) or getattr(root_stat, "st_file_attributes", 0) & 0x400:
        raise ValueError("请选择实际目录，根路径不能是链接或重解析点")
    if not stat.S_ISDIR(root_stat.st_mode):
        raise ValueError("扫描目标必须是目录")
    started = time.monotonic()
    totals = Counter()
    extensions = Counter()
    largest = []
    stack = [(root, 0)]
    visited = []
    samples = []
    files = links = errors = duplicates = 0
    seen = set()
    interrupted = False
    stop_reason = None
    depth_skipped = deepest = 0
    last_progress = started

    def issue(path, error):
        nonlocal errors
        errors += 1
        if len(samples) < 50:
            samples.append({"path": path, "error": str(error)})

    try:
        while stack:
            if max_seconds is not None and time.monotonic() - started >= max_seconds:
                stop_reason = "time_limit"
                break
            if max_files is not None and files >= max_files:
                stop_reason = "file_limit"
                break
            current, depth = stack.pop()
            deepest = max(deepest, depth)
            visited.append(current)
            try:
                with os.scandir(io_path(current)) as entries:
                    for entry in entries:
                        if max_seconds is not None and time.monotonic() - started >= max_seconds:
                            stop_reason = "time_limit"
                            break
                        if max_files is not None and files >= max_files:
                            stop_reason = "file_limit"
                            break
                        if progress and time.monotonic() - last_progress >= 1:
                            progress(len(visited), files)
                            last_progress = time.monotonic()
                        path = os.path.join(current, entry.name)
                        try:
                            info = entry.stat(follow_symlinks=False)
                            if stat.S_ISLNK(info.st_mode) or getattr(info, "st_file_attributes", 0) & 0x400:
                                links += 1
                                continue
                            if stat.S_ISDIR(info.st_mode):
                                if max_depth is not None and depth >= max_depth:
                                    depth_skipped += 1
                                else:
                                    stack.append((path, depth + 1))
                            elif stat.S_ISREG(info.st_mode):
                                identity = (info.st_dev, info.st_ino)
                                if info.st_ino and info.st_nlink > 1:
                                    if identity in seen:
                                        duplicates += 1
                                        continue
                                    seen.add(identity)
                                files += 1
                                totals[current] += info.st_size
                                extensions[Path(entry.name).suffix.lower() or "(无后缀)"] += info.st_size
                                item = (info.st_size, path)
                                if len(largest) < top:
                                    heapq.heappush(largest, item)
                                elif item > largest[0]:
                                    heapq.heapreplace(largest, item)
                        except OSError as exc:
                            issue(path, exc)
            except OSError as exc:
                issue(current, exc)
            if stop_reason:
                break
            if progress and len(visited) % 100 == 0:
                progress(len(visited), files)
    except KeyboardInterrupt:
        interrupted = True

    # Reverse traversal aggregates children into parents without recursion.
    for current in reversed(visited):
        if current != root:
            totals[os.path.dirname(current)] += totals[current]
    directories = heapq.nlargest(top, ((totals[path], path) for path in visited if path != root))
    return {
        "root": root, "status": "interrupted" if interrupted else "partial" if errors or links or depth_skipped or stop_reason else "complete",
        "stop_reason": "user_cancelled" if interrupted else stop_reason,
        "max_depth": max_depth, "deepest_scanned": deepest,
        "depth_skipped_directories": depth_skipped,
        "pending_directories": len(stack),
        "bytes": totals[root], "files": files, "directories": len(visited),
        "skipped_links": links, "duplicate_hardlinks": duplicates,
        "errors": errors, "error_samples": samples,
        "elapsed_seconds": round(time.monotonic() - started, 2),
        "largest_files": [{"path": path, "bytes": size, "suggestion": advice(path)}
                          for size, path in sorted(largest, reverse=True)],
        "largest_directories": [{"path": path, "bytes": size} for size, path in directories],
        "extensions": [{"extension": ext, "bytes": size} for ext, size in extensions.most_common()],
    }


def render_report(result):
    def table(items, kind):
        rows = []
        for item in items:
            label = item.get("path", item.get("extension", ""))
            suggestion = item.get("suggestion", "")
            rows.append(f"<tr><td>{html.escape(label)}</td><td>{human_size(item['bytes'])}</td>"
                        f"<td>{html.escape(suggestion)}</td></tr>")
        return f"<h2>{kind}</h2><table><tr><th>位置 / 类型</th><th>大小</th><th>检查建议</th></tr>" + "".join(rows) + "</table>"
    issues = "".join(f"<li>{html.escape(item['path'])}：{html.escape(item['error'])}</li>"
                     for item in result["error_samples"])
    return f"""<!doctype html><html lang="zh-CN"><meta charset="utf-8">
<title>磁盘空间分析助手</title><style>
body{{font-family:Segoe UI,Microsoft YaHei,sans-serif;background:#f3f5f9;color:#18263c;max-width:1100px;margin:40px auto;padding:0 24px}}
header,section{{background:white;border-radius:16px;padding:24px;margin:20px 0}}h1{{margin-top:0}}
table{{border-collapse:collapse;width:100%;font-size:14px}}td,th{{padding:12px;border-bottom:1px solid #e4e8ef;text-align:left;overflow-wrap:anywhere}}td:nth-child(2){{white-space:nowrap}}
.stats{{font-size:20px;color:#275abe}}p{{line-height:1.7}}li{{overflow-wrap:anywhere}}
</style><header><h1>磁盘空间分析助手</h1><p>{html.escape(result['root'])}</p>
<p class="stats">已统计 {human_size(result['bytes'])} · {result['files']:,} 个文件 · {result['elapsed_seconds']} 秒</p>
<p>状态：{result['status']}；无法读取 {result['errors']} 项；跳过链接/重解析点 {result['skipped_links']} 项；硬链接去重 {result['duplicate_hardlinks']} 项。</p>
<p>最深已扫描 {result.get('deepest_scanned', 0)} 层（根目录为 0）；深度限制跳过 {result.get('depth_skipped_directories', 0)} 个目录；待扫描 {result.get('pending_directories', 0)} 个目录；停止原因：{html.escape(result.get('stop_reason') or '正常结束')}。被跳过的目录大小未知，未计入总量。</p>
<p>大小为可读取文件的逻辑字节数，不等于磁盘实际分配空间。目录大小包含子目录，排行各行不可相加。建议来自本地后缀规则，尚未接入 AI；不能作为删除许可。扫描过程中变化的文件可能造成统计偏差。</p></header>
<section>{table(result['largest_directories'], '大目录')}{table(result['largest_files'], '大文件')}{table(result['extensions'][:20], '文件类型占用')}</section>
<section><h2>无法读取的位置（最多展示 50 项）</h2><ul>{issues or '<li>未记录读取错误</li>'}</ul></section></html>"""


def main():
    parser = argparse.ArgumentParser(description="磁盘空间分析助手：只读扫描任意盘符或目录")
    parser.add_argument("directory", help="例如 D:\\ 或 D:\\Downloads")
    parser.add_argument("--top", type=int, default=20)
    parser.add_argument("--max-depth", type=int, help="根目录为 0；默认不限层数")
    parser.add_argument("--max-seconds", type=float, help="扫描时间上限，单位秒")
    parser.add_argument("--max-files", type=int, help="最多统计的文件数量")
    parser.add_argument("--report", type=Path, help="将可视化报告保存为 HTML")
    parser.add_argument("--json", type=Path, help="将扫描数据保存为 JSON")
    args = parser.parse_args()
    if args.top < 1:
        parser.error("--top 必须至少为 1")
    # Output must be a new file; never replace personal files.
    for output in (args.report, args.json):
        if output and output.exists():
            parser.error(f"报告已存在，请使用新文件名：{output}")
    try:
        result = scan(args.directory, args.top,
                      lambda dirs, count: print(f"已扫描 {dirs:,} 个目录 / {count:,} 个文件…", file=sys.stderr),
                      max_depth=args.max_depth, max_seconds=args.max_seconds, max_files=args.max_files)
        print(f"{result['root']}\n状态：{result['status']}\n已统计：{human_size(result['bytes'])} / {result['files']:,} 个文件")
        print("\n大文件：")
        for item in result["largest_files"]:
            print(f"{human_size(item['bytes']):>12}  {item['path']}")
        print("\n大目录（包含子目录，不可相加）：")
        for item in result["largest_directories"]:
            print(f"{human_size(item['bytes']):>12}  {item['path']}")
        print(f"读取错误：{result['errors']}；跳过链接：{result['skipped_links']}")
        print(f"最深扫描：{result['deepest_scanned']} 层；深度跳过：{result['depth_skipped_directories']}；停止原因：{result['stop_reason'] or '正常结束'}")
        for output, content in ((args.report, render_report(result)),
                                (args.json, json.dumps(result, ensure_ascii=False, indent=2))):
            if output:
                with output.open("x", encoding="utf-8") as stream:
                    stream.write(content)
                print(f"报告已保存：{output.absolute()}")
    except (OSError, ValueError) as exc:
        parser.exit(1, f"扫描或保存失败：{exc}\n")


if __name__ == "__main__":
    main()
