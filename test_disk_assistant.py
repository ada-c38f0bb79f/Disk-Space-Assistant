import os
from pathlib import Path
import tempfile
import unittest
import stat
from types import SimpleNamespace
from unittest.mock import patch

from disk_assistant import scan, render_report


class ScanTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(dir=Path(__file__).parent)
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "child").mkdir()
        (self.root / "a.txt").write_bytes(b"abc")
        (self.root / "child/b.csv").write_bytes(b"12345")

    def test_recursive_totals_and_no_modification(self):
        result = scan(self.root, 1)
        self.assertEqual(result['bytes'], 8)
        self.assertEqual(result['files'], 2)
        self.assertEqual(result['largest_directories'][0]['bytes'], 5)
        self.assertEqual(result['largest_files'][0]['bytes'], 5)
        self.assertEqual((self.root / 'a.txt').read_bytes(), b'abc')

    def test_permission_failure_is_visible(self):
        original = os.scandir
        def fail_child(path):
            if Path(path).name == 'child':
                raise PermissionError('test denied')
            return original(path)
        with patch('disk_assistant.os.scandir', side_effect=fail_child):
            result = scan(self.root)
        self.assertEqual(result['status'], 'partial')
        self.assertEqual(result['bytes'], 3)
        self.assertEqual(result['errors'], 1)

    def test_hardlink_not_double_counted(self):
        try:
            os.link(self.root / 'a.txt', self.root / 'copy.txt')
        except OSError:
            self.skipTest('hardlinks unavailable')
        result = scan(self.root)
        self.assertEqual(result['bytes'], 8)
        self.assertEqual(result['duplicate_hardlinks'], 1)

    def test_html_escapes_paths(self):
        result = scan(self.root)
        result['root'] = '<script>alert(1)</script>'
        report = render_report(result)
        self.assertNotIn('<script>', report)
        self.assertIn('&lt;script&gt;', report)

    def test_file_root_rejected(self):
        with self.assertRaises(ValueError):
            scan(self.root / 'a.txt')

    def test_depth_zero_counts_only_root_files(self):
        result = scan(self.root, max_depth=0)
        self.assertEqual(result['bytes'], 3)
        self.assertEqual(result['status'], 'partial')
        self.assertEqual(result['depth_skipped_directories'], 1)

    def test_file_limit_reports_partial(self):
        result = scan(self.root, max_files=1)
        self.assertEqual(result['files'], 1)
        self.assertEqual(result['stop_reason'], 'file_limit')

    def test_time_limit_reports_partial(self):
        with patch('disk_assistant.time.monotonic', side_effect=[0, 2, 3]):
            result = scan(self.root, max_seconds=1)
        self.assertEqual(result['status'], 'partial')
        self.assertEqual(result['stop_reason'], 'time_limit')

    def test_1500_levels_without_recursion(self):
        from contextlib import nullcontext
        root = str(self.root)
        def entries(path):
            readable = path[4:] if path.startswith('\\\\?\\') else path
            depth = len(os.path.relpath(readable, root).split(os.sep)) if readable != root else 0
            is_dir = depth < 1500
            info = SimpleNamespace(st_mode=stat.S_IFDIR if is_dir else stat.S_IFREG,
                                   st_file_attributes=0, st_size=7, st_dev=1, st_ino=1, st_nlink=1)
            entry = SimpleNamespace(name='d' if is_dir else 'leaf.txt',
                                    stat=lambda **kwargs: info)
            return nullcontext(iter([entry]))
        with patch('disk_assistant.os.scandir', side_effect=entries):
            result = scan(self.root)
        self.assertEqual(result['deepest_scanned'], 1500)
        self.assertEqual(result['bytes'], 7)
        self.assertEqual(result['directories'], 1501)

    def test_link_cycle_is_skipped(self):
        from contextlib import nullcontext
        info = SimpleNamespace(st_mode=stat.S_IFLNK, st_file_attributes=0)
        entry = SimpleNamespace(name='loop', stat=lambda **kwargs: info)
        with patch('disk_assistant.os.scandir', return_value=nullcontext(iter([entry]))):
            result = scan(self.root)
        self.assertEqual(result['skipped_links'], 1)
        self.assertEqual(result['directories'], 1)


if __name__ == '__main__':
    unittest.main()
