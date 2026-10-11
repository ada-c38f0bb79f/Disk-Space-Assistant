# 磁盘空间分析助手 / Disk Space Assistant

[English](README.en.md)

支持任意盘符或文件夹的本地空间分析工具。找出大文件、大目录和文件类型占用，生成中文 HTML 报告。提供 Windows 窗口版和命令行版。

**v0.2.0 MVP：只读扫描、可交互空间图和清理候选；AI 解释尚未接入。**

## 下载

[下载 Windows 便携版](https://github.com/ada-c38f0bb79f/agent-runtime-research/releases/tag/v0.2.0)

解压后双击 `DiskSpaceAssistant.exe`，选择目录与报告保存位置，扫描完成后点击“打开报告”。无需安装 Python。`DiskSpaceAssistantCLI.exe` 为命令行版。

面向 Windows x64，未数字签名；窗口交互及其他设备兼容性尚未验证。

## 功能

报告加入空间分布交互图：点击目录下钻、返回上级；候选文件可按风险类别和路径筛选。最大 200 个候选依据路径与后缀生成，显示判断理由与潜在影响；未确认可恢复性，不提供删除按钮。

- 只读迭代遍历，避免 Python 递归层数限制。
- Windows 长路径处理，跳过符号链接和重解析点。
- 大文件/目录排行、文件类型占用、硬链接去重。
- 深度、时间、文件数量上限，HTML/JSON 报告和读取错误记录。
- 桌面目录选择、扫描进度及报告打开。

## 源码运行

Python 3.10+，标准库；窗口版需要 Tkinter。

```powershell
python disk_assistant_desktop.py
python disk_assistant.py D:/ --report report-d.html
python disk_assistant.py D:/ --max-depth 4 --max-seconds 60 --max-files 100000 --report preview-d.html
python disk_assistant.py "C:\Users" --json report-users.json
python -m unittest -v test_disk_assistant
```

报告使用新文件名，不覆盖已有文件。根目录为第 0 层，默认不限深度。命令行 Ctrl+C 可保存部分统计；关闭桌面窗口会结束扫描。

## 统计口径与限制

统计为逻辑字节数，不等于实际磁盘占用。目录包含子目录，排行不可相加。权限错误、截断、链接跳过及变化中的文件可能导致结果不完整。时间限制无法中断阻塞的系统调用；内存随已访问和待扫描目录数增长。

后缀建议不代表可以删除。程序不清理文件、不读取文件内容、不发送数据到网络。报告包含本地路径，请按个人信息保管。

## 验证与计划

扫描测试 12 项通过、1 项硬链接测试因环境限制跳过，包含模拟 1,500 层目录、链接循环、统计、读取错误、扫描上限、目录汇总、候选保护和 HTML 转义。

下一步：基于用户确认和脱敏的扫描摘要加入 AI 解释，再考虑确认后的清理。

仓库只维护当前产品。旧研究材料已从当前分支移除，可从 Git 历史找回。详见 [Release 说明](RELEASE_NOTES.md)。
