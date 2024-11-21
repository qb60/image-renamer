import unittest
from img_renamer import convert_exif_date_to_date_parts


class TestExifDate(unittest.TestCase):
    def test_get_proper_exif_date(self):
        exif_date = "2019:10:28 17:33:15"
        expected_match = {'YYYY': '2019', 'MM': '10', 'DD': '28', 'HH': '17', 'mm': '33', 'ss': '15'}

        match = convert_exif_date_to_date_parts(exif_date)

        self.assertEqual(match, expected_match)

    def test_get_improper_exif_date(self):
        exif_date = "TESTTEST"
        expected_match = None

        match = convert_exif_date_to_date_parts(exif_date)

        self.assertEqual(match, expected_match)


if __name__ == '__main__':
    unittest.main()
