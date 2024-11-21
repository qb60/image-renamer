import unittest
from unittest.mock import Mock

from img_renamer import rename_files, FsHandler, Options, AppMode


class TestImageRenamer(unittest.TestCase):
    DUMMY_PATH = "TEST"

    def setUp(self):
        self.options = Options(self.DUMMY_PATH, AppMode.NO_EXIF)
        self.fs = Mock(spec=FsHandler)

    def test_pattern_rename(self):
        old_filename = "IMG20180327112259.jpg"
        new_filename = "IMG_20180327_112259.jpg"
        self.fs.get_file_list.return_value = [old_filename]

        [renamed, skipped] = rename_files(self.fs, self.options)

        self.fs.rename_file.assert_called_with(old_filename, new_filename)
        self.assertEqual(renamed, 1)
        self.assertEqual(skipped, 0)

    def test_skip_unknown(self):
        old_filename = "UNKNOWN.jpg"
        self.fs.get_file_list.return_value = [old_filename]

        [renamed, skipped] = rename_files(self.fs, self.options)

        self.assertEqual(renamed, 0)
        self.assertEqual(skipped, 1)

    def test_skip_already_formatted(self):
        old_filename = "IMG_20180327_112259.jpg"
        self.fs.get_file_list.return_value = [old_filename]

        [renamed, skipped] = rename_files(self.fs, self.options)

        self.assertEqual(renamed, 0)
        self.assertEqual(skipped, 1)

    def test_exif_for_all(self):
        old_filename = "IMG_20180327_112259.jpg"
        new_filename = "IMG_20220102_030405.jpg"
        self.options.mode = AppMode.EXIF_FOR_ALL
        self.fs.get_file_list.return_value = [old_filename]
        self.fs.get_exif_date.return_value = {'YYYY': '2022', 'MM': '01', 'DD': '02', 'HH': '03', 'mm': '04', 'ss': '05'}

        [renamed, skipped] = rename_files(self.fs, self.options)

        self.fs.rename_file.assert_called_with(old_filename, new_filename)
        self.assertEqual(renamed, 1)
        self.assertEqual(skipped, 0)

    def test_exif_for_unknown_name(self):
        old_filename1 = "UNKNOWN.jpg"
        new_filename1 = "IMG_20220102_030405.jpg"

        old_filename2 = "IMG20180327112259.jpg"
        new_filename2 = "IMG_20180327_112259.jpg"

        self.options.mode = AppMode.EXIF_FOR_UNKNOWN
        self.fs.get_file_list.return_value = [old_filename1, old_filename2]
        self.fs.get_exif_date.return_value = {'YYYY': '2022', 'MM': '01', 'DD': '02', 'HH': '03', 'mm': '04', 'ss': '05'}

        [renamed, skipped] = rename_files(self.fs, self.options)

        self.fs.rename_file.assert_any_call(old_filename1, new_filename1)
        self.fs.rename_file.assert_any_call(old_filename2, new_filename2)
        self.assertEqual(renamed, 2)
        self.assertEqual(skipped, 0)

    def test_no_exif_data_but_suitable_name(self):
        old_filename = "IMG20180327112259.jpg"
        new_filename = "IMG_20180327_112259.jpg"
        self.options.mode = AppMode.EXIF_FOR_ALL
        self.fs.get_file_list.return_value = [old_filename]
        self.fs.get_exif_date.return_value = None

        [renamed, skipped] = rename_files(self.fs, self.options)

        self.fs.rename_file.assert_called_with(old_filename, new_filename)
        self.assertEqual(renamed, 1)
        self.assertEqual(skipped, 0)


if __name__ == '__main__':
    unittest.main()
