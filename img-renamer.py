#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
from datetime import datetime

# Define the output format as a constant
OUTPUT_FORMAT = "IMG_{YYYY}{MM}{DD}_{hh}{mm}{ss}{suffix}"

# Updated patterns without trailing dots and asterisks
patterns = [
    r'IMG{YYYY}{MM}{DD}{hh}{mm}{ss}',
    r'IMG_{DD}-{MM}-{YYYY}_{hh}-{mm}-{ss}',
    r'IMG_{YYYY}{MM}{DD}_{hh}{mm}{ss}',
    r'PXL_{DD}-{MM}-{YYYY}_{hh}-{mm}-{ss}',
    r'PXL_{YYYY}{MM}{DD}_{hh}{mm}{ss}',
    r'SK_{YYYY}{MM}{DD}_{hh}{mm}{ss}'
]

def create_regex_pattern(pattern):
    return pattern.replace(
        '{YYYY}', r'(?P<YYYY>\d{4})').replace(
        '{MM}', r'(?P<MM>\d{2})').replace(
        '{DD}', r'(?P<DD>\d{2})').replace(
        '{hh}', r'(?P<hh>\d{2})').replace(
        '{mm}', r'(?P<mm>\d{2})').replace(
        '{ss}', r'(?P<ss>\d{2})') + r'.*'  # Add '.*' at the end to match any trailing characters

# Convert human-readable patterns to regex patterns
regex_patterns = [create_regex_pattern(pattern) for pattern in patterns]

def rename_file(filename, existing_files):
    name, ext = os.path.splitext(filename)
    for pattern in regex_patterns:
        match = re.match(pattern, name)
        if match:
            date_parts = match.groupdict()
            suffix = ""
            counter = 1
            while True:
                new_name = OUTPUT_FORMAT.format(**date_parts, suffix=suffix) + ext
                if new_name not in existing_files:
                    return new_name
                suffix = f"_{counter}"
                counter += 1
    return None

def main():
    folder_path = '.'  # Current directory, change if needed
    renamed_count = 0
    skipped_count = 0
    existing_files = set(os.listdir(folder_path))
    
    for filename in list(existing_files):
        if filename.lower().endswith('.jpg'):
            new_name = rename_file(filename, existing_files)
            if new_name and new_name != filename:
                old_path = os.path.join(folder_path, filename)
                new_path = os.path.join(folder_path, new_name)
                try:
                    os.rename(old_path, new_path)
                    print(f"Renamed: {filename} -> {new_name}")
                    renamed_count += 1
                    existing_files.remove(filename)
                    existing_files.add(new_name)
                except OSError as e:
                    print(f"Error renaming {filename}: {e}")
                    skipped_count += 1
            else:
                print(f"Skipped: {filename} (no match or already in correct format)")
                skipped_count += 1
    
    print(f"\nSummary:")
    print(f"Total files renamed: {renamed_count}")
    print(f"Total files skipped: {skipped_count}")

if __name__ == "__main__":
    main()
