# Image Renamer

A simple Python script to rename image files based on their timestamp information.

## Description

This script renames image files in the given directory to a standardized format: `IMG_YYYYMMDD_HHmmss.jpg`. It supports various input filename formats and handles potential naming conflicts by adding a numeric suffix when necessary. Also, it can take date timestamp from EXIF (`datetime` field only).

## Usage
```
img_renamer.py [-h] [-e] [-u] [PATH]

positional arguments:
  PATH                  path to files for renaming, current directory if not given

options:
  -h, --help               show this help message and exit
  -e, --exif               take data from exif for all files
  -u, --exif-for-unknown   take data from exif for files with unknown name format only
```

The script will process .jpg files in the given directory and rename them according to the specified format.

## Requirements

- Python 3.x