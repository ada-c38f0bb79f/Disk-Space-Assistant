from pathlib import Path
import tempfile
import unittest
from disk_assistant import scan
from scan_index import directory_page
from cleanup_actions import validate_recycle


class IndexTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(dir=Path(__file__).parent)
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def test_full_index_not_limited_to_top_files(self):
        source = self.root / 'source'
        source.mkdir()
        for i in range(12):
            (source / f'{i}.zip').write_bytes(b'x' * (i + 1))
        index = self.root / 'scan.sqlite'
        result = scan(source, top=2, index_path=index)
        self.assertEqual(len(result['largest_files']), 2)
        total, page, children = directory_page(index, str(source), page_size=5)
        self.assertEqual(total, 12)
        self.assertEqual(len(page), 5)
        self.assertEqual(page[0]['bytes'], 12)
        _, second, _ = directory_page(index, str(source), page=1, page_size=5)
        self.assertEqual(second[0]['bytes'], 7)

    def test_recycle_validation_never_deletes(self):
        path = self.root / 'archive.zip'
        path.write_bytes(b'123')
        self.assertEqual(validate_recycle({'path': str(path), 'bytes': 3}), path)
        with self.assertRaises(ValueError):
            validate_recycle({'path': str(path), 'bytes': 4})
        self.assertTrue(path.exists())

    def test_unknown_file_protected(self):
        path = self.root / 'database.db'
        path.write_bytes(b'123')
        with self.assertRaises(ValueError):
            validate_recycle({'path': str(path), 'bytes': 3})
        self.assertTrue(path.exists())


if __name__ == '__main__':
    unittest.main()
