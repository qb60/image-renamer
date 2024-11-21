#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import argparse
import sys

from exif import Image

OUTPUT_FORMAT = "IMG_{YYYY}{MM}{DD}_{HH}{mm}{ss}"

INPUT_FORMATS = [
    "{YYYY}{MM}{DD}_{HH}{mm}{ss}",
    "IMG{YYYY}{MM}{DD}{HH}{mm}{ss}",
    "IMG_{DD}-{MM}-{YYYY}_{HH}-{mm}-{ss}",
    "IMG_{YYYY}{MM}{DD}_{HH}{mm}{ss}",
    "PXL_{DD}-{MM}-{YYYY}_{HH}-{mm}-{ss}",
    "PXL_{YYYY}{MM}{DD}_{HH}{mm}{ss}",
    "SK_{YYYY}{MM}{DD}_{HH}{mm}{ss}"
]

EXT = ".jpg"
EXIF_FORMAT = "{YYYY}:{MM}:{DD} {HH}:{mm}:{ss}"


def create_regex_pattern(pattern):
    return (pattern.replace(
        '{YYYY}', r'(?P<YYYY>\d{4})').replace(
        '{MM}', r'(?P<MM>\d{2})').replace(
        '{DD}', r'(?P<DD>\d{2})').replace(
        '{HH}', r'(?P<HH>\d{2})').replace(
        '{mm}', r'(?P<mm>\d{2})').replace(
        '{ss}', r'(?P<ss>\d{2})') + r'.*')  # Add '.*' at the end to match any trailing characters


regex_input_patterns = [create_regex_pattern(pattern) for pattern in INPUT_FORMATS]
regex_output_pattern = create_regex_pattern(OUTPUT_FORMAT)


def rename_file_with_pattern(filename, existing_files):
    name, ext = os.path.splitext(filename)

    if re.match(regex_output_pattern, name):
        return filename

    for pattern in regex_input_patterns:
        match = re.match(pattern, name)
        if match:
            date_parts = match.groupdict()
            return convert_date_to_unique_name(date_parts, filename, existing_files, ext)
    return None


def rename_file_with_exif(filename, existing_files, date_parts):
    _, ext = os.path.splitext(filename)
    new_name = convert_date_to_unique_name(date_parts, filename, existing_files, ext)
    return new_name


def convert_date_to_unique_name(date_parts, old_filename, existing_files, ext):
    new_name_prefix = OUTPUT_FORMAT.format(**date_parts)

    if new_name_prefix + ext == old_filename:
        return old_filename

    return deduplicate_filename(new_name_prefix, existing_files, ext)


def deduplicate_filename(new_filename_prefix, existing_files, ext):
    suffix = ""
    counter = 1
    while True:
        new_name = new_filename_prefix + suffix + ext
        if new_name not in existing_files:
            return new_name
        suffix = f"_{counter}"
        counter += 1


def convert_exif_date_to_date_parts(exif_date: str):
    exif_pattern = create_regex_pattern(EXIF_FORMAT)
    match = re.match(exif_pattern, exif_date)
    if not match:
        return None
    else:
        return match.groupdict()


class FsHandler:
    def __init__(self, path):
        self.path = path

    def get_file_list(self):
        return os.listdir(self.path)

    def __get_full_path(self, filename):
        return os.path.join(self.path, filename)

    def get_exif_date(self, filename):
        with open(self.__get_full_path(filename), 'rb') as image_file:
            image = Image(image_file)
            if image.get("datetime"):
                return convert_exif_date_to_date_parts(image.datetime)
            else:
                return None

    def rename_file(self, old_name, new_name):
        old_path = self.__get_full_path(old_name)
        new_path = self.__get_full_path(new_name)
        os.rename(old_path, new_path)


class AppMode:
    NO_EXIF = 1,
    EXIF_FOR_ALL = 2,
    EXIF_FOR_UNKNOWN = 3


class Options:
    def __init__(self, path: str, mode: int):
        self.path = path
        self.mode = mode


def rename_files(fs_handler: FsHandler, options: Options) -> [int, int]:
    renamed_count = 0
    skipped_count = 0
    existing_files = set(fs_handler.get_file_list())

    for filename in list(existing_files):
        if filename.lower().endswith(EXT):
            new_name = None
            date_taken_from = ""
            if options.mode != AppMode.EXIF_FOR_ALL:
                new_name = rename_file_with_pattern(filename, existing_files)
                date_taken_from = "date from filename"

            is_not_suitable_name_but_exif_enabled = new_name is None and options.mode == AppMode.EXIF_FOR_UNKNOWN
            if options.mode == AppMode.EXIF_FOR_ALL or is_not_suitable_name_but_exif_enabled:
                date_parts = fs_handler.get_exif_date(filename)
                if date_parts is not None:
                    new_name = rename_file_with_exif(filename, existing_files, date_parts)
                    date_taken_from = "date from exif"
                else:
                    new_name = rename_file_with_pattern(filename, existing_files)
                    date_taken_from = "no EXIF date, but suitable filename"
                    if new_name is None:
                        print(f"Skipped: {filename} (No EXIF date)")
                        skipped_count += 1
                        continue

            if not new_name:
                print(f"Skipped: {filename} (unknown filename format)")
                skipped_count += 1
                continue

            if new_name == filename:
                print(f"Skipped: {filename} (already in proper format)")
                skipped_count += 1
                continue

            try:
                fs_handler.rename_file(filename, new_name)
                existing_files.remove(filename)
                existing_files.add(new_name)

                print(f"Renamed: {filename} -> {new_name} ({date_taken_from})")
                renamed_count += 1

            except OSError as e:
                skipped_count += 1
                print(f"Error renaming {filename}: {e}")

    return [renamed_count, skipped_count]


def parse_arguments(argv: [str]):
    parser = argparse.ArgumentParser()
    parser.add_argument("PATH", nargs="?", help="path to files for renaming", default=".")
    parser.add_argument("-e", "--exif", dest="exif_for_all", action="store_true",
                        help="take data from exif for all files")
    parser.add_argument("-u", "--exif-for-unknown", action="store_true",
                        help="take data from exif for files with unknown name format only")

    raw_options = parser.parse_args(argv)
    if raw_options.exif_for_all and raw_options.exif_for_unknown:
        parser.error("-e and -u can't be used simultaneously")

    if raw_options.exif_for_all:
        mode = AppMode.EXIF_FOR_ALL
    elif raw_options.exif_for_unknown:
        mode = AppMode.EXIF_FOR_UNKNOWN
    else:
        mode = AppMode.NO_EXIF

    return Options(raw_options.PATH, mode)


def main():
    options = parse_arguments(sys.argv[1:])

    if options.mode == AppMode.EXIF_FOR_ALL:
        print("Mode: EXIF date for all filenames")
    elif options.mode == AppMode.EXIF_FOR_UNKNOWN:
        print("Mode: EXIF date for unknown filenames")
    else:
        print("Mode: date from filenames only")

    fs_handler = FsHandler(options.path)
    [renamed_count, skipped_count] = rename_files(fs_handler, options)

    print(f"\nSummary:")
    print(f"Total files renamed: {renamed_count}")
    print(f"Total files skipped: {skipped_count}")


if __name__ == "__main__":
    main()
