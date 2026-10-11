# Disk Space Assistant

[简体中文](README.md) · [Windows preview v0.6.0](https://github.com/ada-c38f0bb79f/Disk-Space-Assistant/releases/tag/v0.6.0)

A Windows desktop disk space analyzer with directory totals, hierarchical browsing, colored usage charts, optional cloud AI explanations and user-confirmed recycling.

## Workflow

Extract and launch `DiskSpaceAssistant.exe`; Python is not required.

1. Select a drive and scan it, or choose a folder. A highlighted scope banner distinguishes a whole drive from a folder such as `C:\Users`.
2. Overview cards show scanned logical bytes, file count, read errors and AI coverage. The sidebar shows current system disk usage, which uses a different measurement.
3. Browse directories and file pages (100 entries per page) through a local SQLite index. Click headings to sort by name or size. Colors vary by drive and subdirectory.
4. Select 1–20 files for AI analysis. Global API settings are shared within the current session. Requests process up to five items per batch; completed results survive later failures.
5. Import earlier HTML reports or export results. Missing detail in old reports requires rescanning.

## AI and recycling

`chat` supports compatible Chat Completions services such as DeepSeek and provides unsearched inference. `search` requires Responses `web_search` support and retains actual citations. Models must be available to your account.

Requests require confirmation of a redacted metadata preview; filenames/context can still contain personal information. File contents are not uploaded. API/search may incur charges. Keys remain in session memory, are not written to disk, and are validated for invalid characters.

Recycle one file only after explicit confirmation. Protected/unknown items, directories, links, changed-size files and non-fixed local drives are rejected. No permanent-delete fallback. Recycling has not been exercised on personal files and may not immediately release disk space. AI explanations do not prove deletion safety. Rescan after changes.

## Development

Python 3.10+ with Tkinter. Windows recycling requires Send2Trash and pywin32.

```powershell
python -m pip install -r requirements.txt
python disk_assistant_desktop.py
python disk_assistant.py D:/ --report report-d.html
python -m unittest -v test_disk_assistant test_cloud_analysis test_file_records test_scan_index test_desktop_theme
node test_report_visual.js
```

Sizes are logical bytes, not allocated space. Parent totals include children. Permissions, skipped links, limits and changing files can cause incomplete results. Deadlines cannot interrupt blocked filesystem calls.

Unsigned preview. Full GUI interaction, live multi-batch API calls and other-machine compatibility remain unverified. Interface/reports currently use Chinese; this document provides English guidance. Personal reports and indexes are excluded from Git. See [release notes](RELEASE_NOTES.md).
