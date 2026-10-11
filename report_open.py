"""Open local reports in an explicit browser, never a default homepage."""
import os
from pathlib import Path
import subprocess


def open_report(path):
    report = Path(path).resolve(strict=True)
    candidates = []
    for base in (os.environ.get('ProgramFiles(x86)', ''), os.environ.get('ProgramFiles', ''), os.environ.get('LOCALAPPDATA', '')):
        if base:
            candidates.extend([Path(base) / 'Microsoft/Edge/Application/msedge.exe',
                               Path(base) / 'Google/Chrome/Application/chrome.exe'])
    for browser in candidates:
        if browser.is_file():
            subprocess.Popen([str(browser), report.as_uri()])
            return str(browser)
    raise ValueError('未找到 Edge 或 Chrome。请将报告拖入你选择的浏览器：' + str(report))
