import unittest
from desktop_theme import scope_message, drive_colors


class ThemeTests(unittest.TestCase):
    def test_folder_not_mislabeled_as_whole_drive(self):
        self.assertIn('仅扫描文件夹', scope_message('C:\\Users'))
        self.assertIn('整盘扫描范围', scope_message('C:\\'))
        self.assertIn('整盘扫描范围', scope_message('D:/'))

    def test_partition_colors_are_stable_and_distinct(self):
        self.assertEqual(drive_colors('C:/'), drive_colors('C:/Users'))
        self.assertNotEqual(drive_colors('C:/')[0], drive_colors('D:/')[0])
        self.assertEqual(len(set(drive_colors('C:/'))), 12)


if __name__ == '__main__':
    unittest.main()
