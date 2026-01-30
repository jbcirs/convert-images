# CLAUDE.md

## Project Overview

Image converter tool that accepts a wide range of input image formats and converts them to PNG, JPG/JPEG, or PDF. Uses Pillow and pillow-heif for image processing and ReportLab for PDF generation. No external binaries required.

## Repo Structure

```
convert-images/
├── CLAUDE.md               # This file
├── README.md               # User-facing documentation
├── requirements.txt        # Python dependencies
├── setup.py                # Dependency installer and directory setup
├── .gitignore
├── images/
│   ├── source/             # Drop input images here
│   │   └── README.md
│   └── output/             # Converted files land here
│       └── README.md
├── logs/                   # Timestamped log files (auto-created)
├── scripts/
│   ├── convert_heic.sh     # Interactive shell script (Unix/Mac)
│   └── convert_heic.bat    # Interactive batch script (Windows)
└── src/
    ├── convert_heic.py     # Main converter (CLI + library)
    └── example_usage.py    # Programmatic usage examples
```

## Supported Formats

**Input formats:** HEIC, HEIF, AVIF, JPG/JPEG, PNG, BMP, TIFF/TIF, GIF (first frame), WebP, ICO, PPM, PGM, PBM, TGA

**Output formats:** PNG, JPG/JPEG, PDF

## Key Commands

```bash
# Run converter (from project root or src/)
python src/convert_heic.py                    # Default: PNG output
python src/convert_heic.py -f jpg -q 90       # JPG at 90% quality
python src/convert_heic.py -f pdf --page-size a4
python src/convert_heic.py -v                 # Verbose/debug logging

# Run examples
python src/example_usage.py

# Install dependencies
pip install -r requirements.txt
# or
python setup.py
```

## Code Conventions

- Python 3.7+ compatibility
- Docstrings on all public functions (Args/Returns format)
- Logging via stdlib `logging` module (INFO default, DEBUG with `-v`)
- Per-file timing and metadata logged during conversion
- No external binaries; all processing through Python libraries
- Filenames kept as legacy (`convert_heic.py`) for backwards compatibility

## Dependencies

- **pillow-heif**: HEIC/HEIF/AVIF opener (registers with Pillow)
- **Pillow (PIL)**: Core image processing (handles BMP, TIFF, GIF, WebP, ICO, PPM, PGM, PBM, TGA natively)
- **reportlab**: PDF generation

## Testing

No automated test suite. Manual verification:

1. Place sample images of various formats in `images/source/`
2. Run `python src/convert_heic.py -v` and verify log output shows detected format, dimensions, color mode, per-file timing, total elapsed time
3. Run `python src/example_usage.py` and verify imports work without errors
4. Run `python src/convert_heic.py --help` and verify updated description/format list

## Important Notes

- File `src/convert_heic.py` is named for legacy reasons; it handles all supported input formats
- The output folder is cleared before each conversion unless `--no-clear` is passed
- GIF/WebP: only first frame is converted (animated content not supported)
- AVIF support depends on whether libheif was built with AVIF support
- TIFF: first page only for multi-page files
- ICO: opens largest size available
