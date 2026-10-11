# Disk Space Assistant

[简体中文](README.md)

A local disk space analyzer for any drive or folder. Find large files, directory totals and file-type usage, and generate an HTML report. Includes Windows desktop and command-line applications.

**v0.2.0 MVP: read-only scanning, interactive space maps and cleanup candidates. AI explanations are planned.**

## Download

[Windows portable release](https://github.com/ada-c38f0bb79f/agent-runtime-research/releases/tag/v0.2.0)

Extract and launch `DiskSpaceAssistant.exe`. Select a folder and report destination, then open the report after scanning. No Python installation is required. `DiskSpaceAssistantCLI.exe` is the command-line version.

Built for Windows x64 and unsigned. Desktop interaction and compatibility on other machines have not yet been verified. The current interface and reports are in Chinese; English documentation is provided here.

## Features

- Interactive directory drill-down and parent navigation.
- Cleanup candidates filtered by category/path, with evidence and possible impact; no deletion approval or action.

- Read-only iterative traversal, avoiding Python recursion limits.
- Windows extended paths; symbolic links and reparse points are skipped.
- Largest files/directories, extension totals and hardlink deduplication.
- Optional depth, time and file limits; HTML/JSON reports and access-error records.
- Desktop folder selection, progress updates and report opening.

## Run from source

Python 3.10+ and the standard library. Desktop mode also requires Tkinter.

```powershell
python disk_assistant_desktop.py
python disk_assistant.py D:/ --report report-d.html
python disk_assistant.py D:/ --max-depth 4 --max-seconds 60 --max-files 100000 --report preview-d.html
python disk_assistant.py "C:\Users" --json report-users.json
python -m unittest -v test_disk_assistant
```

Use a new report filename; existing files are not overwritten. Root depth is 0 and traversal is unlimited by default. Ctrl+C retains partial statistics in the CLI. Closing the desktop window ends scanning without saving unfinished results.

## Measurement and limitations

Sizes are logical file bytes, not physical allocated space. Parent totals include children; directory-ranking rows must not be added. Permissions, limits, skipped links and changing files can make results incomplete. Time limits cannot interrupt a blocked filesystem call. Memory grows with visited and pending directories.

Extension-based suggestions are not deletion approval. The application does not delete files, read their contents or send data over the network. Reports contain local paths and should be treated as personal information.

## Verification and roadmap

Scanner tests: 12 passed, 1 hardlink test skipped due to the build environment. Coverage includes a simulated 1,500-level hierarchy, link cycles, totals, read failures, scan limits, directory maps, protected paths and HTML escaping.

Next: AI explanations based on reviewed, redacted summaries, followed by user-confirmed cleanup.

This repository now maintains the disk space analyzer. Earlier research documents were removed from the current branch and remain recoverable in Git history. See [release notes](RELEASE_NOTES.md).
