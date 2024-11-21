import unittest
from img_renamer import parse_arguments, AppMode

APP_NAME = "img_renamer.py"


class TestArgumentsParser(unittest.TestCase):
    def test_no_arguments(self):
        args = []
        options = parse_arguments(args)
        self.assertEqual(options.path, ".")

    def test_path_only_argument(self):
        args = ["test_data"]
        options = parse_arguments(args)
        self.assertEqual(options.path, "test_data")

    def test_exif_argument(self):
        args = ["-e"]
        options = parse_arguments(args)
        self.assertEqual(options.mode, AppMode.EXIF_FOR_ALL)

    def test_no_exif_argument(self):
        args = []
        options = parse_arguments(args)
        self.assertEqual(options.mode, AppMode.NO_EXIF)

    def test_exif_for_no_match_argument(self):
        args = ["-u"]
        options = parse_arguments(args)
        self.assertEqual(options.mode, AppMode.EXIF_FOR_UNKNOWN)

    def test_both_exif_options(self):
        args = ["-u", "-e"]
        with self.assertRaises(SystemExit):
            parse_arguments(args)


if __name__ == '__main__':
    unittest.main()
