# 磁盘空间分析助手 / Disk Space Assistant v0.2.0

新增可交互空间图：点击目录逐层查看，返回上级。清理候选支持按风险类别和路径筛选，展示判断依据和影响。保护系统/软件依赖/数据库路径，临时文件只作条件性建议。没有删除功能。新版本需重新扫描生成报告。

New: interactive directory space maps, drill-down, category/path filters for cleanup candidates, reasons and impact. Protected system/dependency/database paths remain in the keep/unknown category. No deletion feature; rescan to create the new report.

12 scanner tests passed; 1 environment-dependent hardlink test skipped. Earlier research documents removed from the current branch; retained in Git history.

发布前验证：v0.2.0 命令行 EXE 成功扫描并生成新版报告；窗口 EXE 完成隐藏初始化自检（退出码 0）。尚未完成实际按钮交互与其他设备兼容性验证。

Release checks: packaged CLI scan/report generation passed; desktop initialization self-test returned exit code 0. Full GUI interaction and other-device compatibility remain unverified.

## English

Read-only disk space analyzer for Windows x64. Extract the archive and launch DiskSpaceAssistant.exe; no Python installation is required. Select a folder, optional depth/time limits and a new HTML report filename. DiskSpaceAssistantCLI.exe supports command-line scanning.

Features: largest files/directories, file-type totals, HTML/JSON reports, Windows long paths, iterative traversal, link skipping and partial-scan/error reporting. The interface and reports currently use Chinese. AI is not connected; suggestions use local rules. No automatic cleanup or network calls.

Unsigned MVP. CLI smoke-tested; desktop interaction and other-machine compatibility have not yet been verified. Logical file sizes differ from allocated space; parent totals include children. Reports contain local paths.

## 中文

双击 DiskSpaceAssistant.exe，选择盘符或文件夹，按需设置最大深度/最长秒数，点击开始扫描，选择新报告文件名。扫描完成后点击“打开报告”。无需安装 Python。

命令行版 DiskSpaceAssistantCLI.exe 示例：

    DiskSpaceAssistantCLI.exe D:/ --max-depth 4 --max-seconds 60 --report report-d.html

功能：只读统计、大文件/大目录排行、文件类型、中文 HTML/可选 JSON、深度与时间/数量限制、链接跳过、读取错误报告、Windows 长路径处理。

大小为可读文件逻辑大小，不等于实际磁盘分配空间。父目录包含子目录，排行不可相加。限制/权限/链接跳过会产生 partial 报告。扫描变化中的文件可能有误差，时间限制不能中断阻塞中的系统调用。

当前解释来自后缀规则，尚未接入 AI。没有自动清理功能、网络请求或付费调用。报告包含文件路径，请自行保管。

桌面版可在扫描期间保持窗口响应；关闭窗口会结束进程，不保存未完成结果。命令行版可用 Ctrl+C 保存部分统计。

构建：Python + PyInstaller 6.11.1；Windows x64。此预发布版本尚未在其他 Windows 设备验证，也未数字签名。
