"""Explicit, user-confirmed recycle only. Never falls back to unlink."""
import os
from pathlib import Path
import stat
from disk_assistant import cleanup_assessment


def validate_recycle(item):
    path = Path(item['path'])
    if not path.is_absolute() or cleanup_assessment(str(path))['level'] == 'keep':
        raise ValueError('该项受保护或用途未知，请通过所属软件处理')
    for ancestor in (path, *path.parents):
        info = os.lstat(ancestor)
        if stat.S_ISLNK(info.st_mode) or getattr(info, 'st_file_attributes', 0) & 0x400:
            raise ValueError('不操作链接或重解析点路径')
    info = path.stat()
    if not stat.S_ISREG(info.st_mode):
        raise ValueError('只允许单个普通文件，不允许删除目录')
    if info.st_size != item['bytes']:
        raise ValueError('文件大小已变化，请重新扫描后确认')
    return path


def recycle(item):
    path = validate_recycle(item)
    if os.name != 'nt':
        raise ValueError('此预览版回收站功能仅支持 Windows')
    import ctypes
    if ctypes.windll.kernel32.GetDriveTypeW(str(path.anchor)) != 3:
        raise ValueError('仅允许本地固定磁盘；网络或移动设备请手动处理')
    # Explicit modern backend: no legacy deletion fallback.
    from send2trash.win.modern import send2trash
    send2trash(str(path))
