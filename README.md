# Image Renamer

A simple Python script to rename image files based on their timestamp information.

## Description

This script renames image files in the current directory to a standardized format: `IMG_YYYYMMDD_hhmmss.jpg`. It supports various input filename formats and handles potential naming conflicts by adding a numeric suffix when necessary.

## Usage

1. Place the `img-renamer.py` script in the directory containing the images you want to rename.
2. Run the script:
   ```
   python3 img-renamer.py
   ```

The script will process all .jpg files in the current directory and rename them according to the specified format.

## Requirements

- Python 3.x