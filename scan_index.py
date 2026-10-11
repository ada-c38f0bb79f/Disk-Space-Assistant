"""Disk-backed per-directory file index; the UI reads pages, not the whole disk."""
import sqlite3
from contextlib import closing


class ScanIndex:
    def __init__(self, path):
        self.connection = sqlite3.connect(path)
        self.connection.execute('CREATE TABLE IF NOT EXISTS files(path TEXT PRIMARY KEY, parent TEXT, name TEXT, bytes INTEGER)')
        self.connection.execute('CREATE INDEX IF NOT EXISTS parent_idx ON files(parent)')
        self.connection.execute('CREATE TABLE IF NOT EXISTS dirs(path TEXT PRIMARY KEY, parent TEXT, bytes INTEGER)')

    def file(self, path, parent, name, size):
        self.connection.execute('INSERT OR REPLACE INTO files VALUES(?,?,?,?)', (path, parent, name, size))

    def finish(self, directories):
        self.connection.executemany('INSERT OR REPLACE INTO dirs VALUES(?,?,?)', directories)
        self.connection.commit()
        self.connection.close()


def directory_page(index_path, directory, page=0, page_size=100, sort='bytes', descending=True):
    if page < 0 or page_size < 1:
        raise ValueError('Invalid page')
    column = 'bytes' if sort == 'bytes' else 'name'
    order = 'DESC' if descending else 'ASC'
    with closing(sqlite3.connect('file:' + __import__('pathlib').Path(index_path).resolve().as_posix() + '?mode=ro', uri=True)) as db:
        total = db.execute('SELECT COUNT(*) FROM files WHERE parent=?', (directory,)).fetchone()[0]
        rows = db.execute(f'SELECT path,name,bytes FROM files WHERE parent=? ORDER BY {column} {order},path LIMIT ? OFFSET ?',
                          (directory, page_size, page * page_size)).fetchall()
        children = db.execute('SELECT path,bytes FROM dirs WHERE parent=? ORDER BY bytes DESC', (directory,)).fetchall()
    return total, [{'path': p, 'name': n, 'bytes': size} for p, n, size in rows], children
