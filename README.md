# 磁盘空间分析助手 / Disk Space Assistant

[English](README.en.md) · [下载 v0.6.0 Windows 预览版](https://github.com/ada-c38f0bb79f/Disk-Space-Assistant/releases/tag/v0.6.0)

查看空间去了哪里，再决定怎么处理。Windows 桌面客户端支持目录总量、分层浏览、彩色占比图、可选云端 AI 文件解释，以及逐项确认的回收站操作。

## 使用

解压后双击 `DiskSpaceAssistant.exe`，无需安装 Python。

1. 在左侧选择盘符并点击“扫描所选整盘”，或扫描指定文件夹。
2. 顶部显示实际扫描范围、逻辑总量、文件数、读取错误和 AI 覆盖。扫描 `C:\Users` 不等于扫描 `C:\`；侧栏整盘容量采用系统实际用量。
3. “目录层级与空间图”可点击下钻、返回上级，文件每页 100 项。名称/大小表头支持排序。完整明细通过本地 SQLite 索引读取。
4. “文件与 AI”选择 1–20 项后分析。API 设置在本次运行内全局复用，模型可选择示例或自行填写。每批最多 5 项，显示已完成数量；后续失败保留之前批次。
5. 可导入旧 HTML 或导出当前结果；旧报告没有保存的文件明细需要重扫。

## AI 与清理

- `chat` 为兼容 Chat Completions 的模型解释，没有联网搜索。DeepSeek 使用此模式。
- `search` 需服务/模型支持 Responses `web_search`，保留实际检索引用。
- 发送前显示脱敏摘要，仍可能包含个人线索；不发送文件内容。API/搜索可能收费。密钥不写入磁盘，退出后清除；中文或空白密钥在本地校验提示。
- “移入回收站”每次一个文件，执行前明确确认路径和影响；拒绝目录、链接、受保护或未知项、大小变化项、非本地固定磁盘。没有永久删除降级。此功能尚未用个人文件实测。
- 回收站不一定立即释放空间；AI 建议不是安全删除证明。空间统计为扫描快照，处理后请重扫。

## 开发与验证

Python 3.10+，Tkinter；Windows 回收站操作需要 Send2Trash / pywin32。

```powershell
python -m pip install -r requirements.txt
python disk_assistant_desktop.py
python disk_assistant.py D:/ --report report-d.html
python -m unittest -v test_disk_assistant test_cloud_analysis test_file_records test_scan_index test_desktop_theme
node test_report_visual.js
```

当前产品测试：28 项通过，1 项硬链接测试因环境限制跳过；另有导出页面的关联、筛选与分页测试。

文件大小为逻辑字节数，不等于系统已分配空间；父目录包含子目录，不能相加。权限、链接跳过、扫描限制和变化中的文件可能使统计不完整。时间限制不能中断阻塞的系统调用。

当前预览版未数字签名；完整鼠标交互、多批真实 API、其他 Windows 设备兼容性仍需验证。个人报告和索引不加入仓库。详见 [云端使用说明](CLOUD_AI.md) 和 [Release 说明](RELEASE_NOTES.md)。
