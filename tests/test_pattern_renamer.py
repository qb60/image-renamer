import unittest
from parameterized import parameterized
from img_renamer import rename_file_with_pattern


class TestPatternRenamer(unittest.TestCase):
    @parameterized.expand([
        # Test case format: (test_name, input_filename, existing_files, expected_output)
        ("test_format_1_basic",
         "IMG20240315123456.jpg",
         set(),
         "IMG_20240315_123456.jpg"),

        ("test_format_2_basic",
         "IMG_15-03-2024_12-34-56.jpg",
         set(),
         "IMG_20240315_123456.jpg"),

        ("test_format_3_basic",
         "IMG_20240315_123456.jpg",
         set(),
         "IMG_20240315_123456.jpg"),

        ("test_format_4_basic",
         "PXL_15-03-2024_12-34-56.jpg",
         set(),
         "IMG_20240315_123456.jpg"),

        ("test_format_5_basic",
         "PXL_20240315_123456.jpg",
         set(),
         "IMG_20240315_123456.jpg"),

        ("test_format_6_basic",
         "SK_20240315_123456.jpg",
         set(),
         "IMG_20240315_123456.jpg"),

        # Test case with existing file (should add suffix)
        ("test_with_existing_file",
         "IMG20240315123456.jpg",
         {"IMG_20240315_123456.jpg"},
         "IMG_20240315_123456_1.jpg"),

        # Test case with multiple existing files
        ("test_with_multiple_existing_files",
         "IMG20240315123456.jpg",
         {"IMG_20240315_123456.jpg", "IMG_20240315_123456_1.jpg"},
         "IMG_20240315_123456_2.jpg"),

        # Test case with non-matching format
        ("test_non_matching_format",
         "random_image.jpg",
         set(),
         None),

        # Test case with extra characters in filename
        ("test_extra_characters",
         "IMG20240315123456_extra_text.jpg",
         set(),
         "IMG_20240315_123456.jpg"),

        ("test_already_in_needed_format",
         "IMG_20240315_123456.jpg",
         {"IMG_20240315_123456.jpg"},
         "IMG_20240315_123456.jpg"),
    ])
    def test_rename_with_pattern(self, _, input_filename, existing_files, expected):
        result = rename_file_with_pattern(input_filename, existing_files)
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
