# Image Converter Tool

A Python utility to convert images from 14+ input formats to PDF, PNG, or JPG with per-file timing, metadata logging, and comprehensive error handling.

## Features

- **14+ input formats**: HEIC, HEIF, AVIF, JPG/JPEG, PNG, BMP, TIFF/TIF, GIF, WebP, ICO, PPM, PGM, PBM, TGA
- **Multiple output formats**: Convert to PDF, PNG, or JPG
- **Batch processing**: Convert all image files from a source folder at once
- **Per-file timing and metadata logging**: Format detection, dimensions, color mode, alpha channel, input file size, elapsed time
- **Quality control**: Adjustable quality settings for JPG output
- **PDF customization**: Choose between Letter and A4 page sizes
- **Automatic setup**: One-command installation of all dependencies
- **Comprehensive logging**: Debug-level logs saved for troubleshooting
- **Cross-platform**: Works on Windows, macOS, and Linux
- **Easy-to-use scripts**: Interactive batch and shell scripts for quick conversion

## Supported Input Formats

| Format | Extensions | Notes |
|--------|------------|-------|
| HEIC/HEIF | `.heic`, `.heif` | Via pillow-heif |
| AVIF | `.avif` | Requires pillow-heif with AVIF support |
| JPEG | `.jpg`, `.jpeg` | Native Pillow |
| PNG | `.png` | Native Pillow |
| BMP | `.bmp` | Native Pillow |
| TIFF | `.tiff`, `.tif` | First page only for multi-page files |
| GIF | `.gif` | First frame only |
| WebP | `.webp` | First frame for animated WebP |
| ICO | `.ico` | Opens largest available size |
| PPM | `.ppm` | Netpbm format, native Pillow |
| PGM | `.pgm` | Netpbm format, native Pillow |
| PBM | `.pbm` | Netpbm format, native Pillow |
| TGA | `.tga` | Native Pillow |

Both lowercase and uppercase extensions are accepted.

**Output formats**: PNG, JPG/JPEG, PDF

## Requirements

- Python 3.7 or higher
- pillow-heif (for HEIC/HEIF/AVIF support)
- Pillow (PIL) (for image processing)
- reportlab (for PDF generation)

## Installation

### Quick Setup

1. Clone or download this repository:

   ```bash
   git clone <repository-url>
   cd convert-images
   ```

2. Run the setup script (automatically installs all dependencies):

   ```bash
   python setup.py
   ```

   The setup script will:
   - Check your Python version
   - Install missing dependencies
   - Create required directories
   - Generate README files

### Manual Installation

If you prefer to install dependencies manually:

```bash
pip install -r requirements.txt
```

## Usage

### Quick Start (Interactive Mode)

The easiest way to use the converter is with the interactive scripts:

**Windows:**
```bash
cd scripts
.\convert_heic.bat
```

**Unix/Linux/macOS:**
```bash
cd scripts
chmod +x convert_heic.sh
./convert_heic.sh
```

These scripts will:
1. Check if dependencies are installed (and run setup if needed)
2. Ask you to choose the output format (PNG, JPG, or PDF)
3. Ask for quality/page size settings
4. Convert all image files from `images/source` to `images/output`

### Command Line Usage

For more control, use the Python script directly:

```bash
cd src
python convert_heic.py [options]
```

#### Basic Examples

```bash
# Convert to PNG (default)
python convert_heic.py

# Convert to JPG with 90% quality
python convert_heic.py -f jpg -q 90

# Convert to PDF with A4 page size
python convert_heic.py -f pdf --page-size a4

# Use custom source and output folders
python convert_heic.py -s /path/to/images -o /path/to/output

# Enable verbose logging for debugging
python convert_heic.py -v

# Keep existing files in output folder (don't clear before conversion)
python convert_heic.py --no-clear
```

#### Command Line Options

- `-s, --source FOLDER`: Source folder containing image files (default: `../images/source`)
- `-o, --output FOLDER`: Output folder for converted files (default: `../images/output`)
- `-f, --format FORMAT`: Output format: `pdf`, `png`, or `jpg` (default: `png`)
- `-q, --quality QUALITY`: JPG quality from 1-100 (default: 95)
- `--page-size SIZE`: PDF page size: `letter` or `a4` (default: `letter`)
- `-v, --verbose`: Enable verbose logging (DEBUG level)
- `--no-clear`: Do not clear output folder before conversion (default: clear enabled)
- `-h, --help`: Show help message and exit

### Programmatic Usage

You can also import and use the converter in your own Python scripts:

```python
from convert_heic import convert_images

# Convert all image files to PNG
stats = convert_images(
    source_folder='images/source',
    output_folder='images/output',
    output_format='PNG',
    quality=95
)

print(f"Converted {stats['successful']} out of {stats['total']} files")
print(f"Elapsed: {stats['elapsed_seconds']:.2f}s")
```

See `src/example_usage.py` for more examples.

## File Organization

```text
convert-images/
├── README.md                    # This file
├── CLAUDE.md                    # Developer reference
├── requirements.txt             # Python dependencies
├── setup.py                     # Setup script
├── LICENSE                      # License file
├── images/
│   ├── source/                  # Place your image files here
│   │   └── README.md
│   └── output/                  # Converted files appear here
│       └── README.md
├── logs/                        # Log files (created automatically)
│   └── convert_images_*.log
├── scripts/                     # Batch and shell scripts
│   ├── convert_heic.bat        # Windows batch script
│   └── convert_heic.sh         # Unix/Linux/macOS shell script
└── src/
    ├── convert_heic.py         # Main conversion script
    └── example_usage.py        # Usage examples
```

## Workflow

1. **Place image files**: Add your images to the `images/source` folder
2. **Run conversion**: Use either the interactive scripts or command line
3. **Check output**: Converted files appear in `images/output` with the same base filename
4. **Review logs**: Check `logs/` folder for detailed conversion information

## How It Works

1. **Cleanup**: Clears the output folder of previous conversions (keeps README)
2. **File Discovery**: Scans the source folder for all supported image files
3. **Format Detection**: Automatically detects files by extension (14+ formats supported)
4. **Metadata Extraction**: Preserves EXIF data from source files
5. **Conversion**: Opens each image file and converts to the target format:
   - **PNG**: Lossless compression, preserves transparency and EXIF metadata
   - **JPG**: High-quality compression with no subsampling, progressive encoding, and EXIF preservation
   - **PDF**: Creates a PDF document with the image scaled to fit the page
6. **Logging**: Records detected format, dimensions, color mode, alpha channel, input file size, per-file timing, and total elapsed time
7. **Output**: Saves converted files with the same base name and new extension

## Logging

Every conversion run creates a timestamped log file in the `logs/` folder:

- **Filename format**: `convert_images_YYYYMMDD_HHMMSS.log`
- **Log levels**: INFO (default) or DEBUG (with `-v` flag)
- **Contents**:
  - Source and output paths
  - Configuration settings
  - Detected input format, dimensions, color mode, alpha channel
  - Input file size
  - Per-file conversion timing
  - Success/failure status with output file sizes
  - Total elapsed time and average time per file
  - Error messages with details

Example log output:
```
2025-11-27 14:30:15 - INFO - Source folder: images/source
2025-11-27 14:30:15 - INFO - Output format: PNG
2025-11-27 14:30:15 - INFO - Found 5 image file(s) to convert
2025-11-27 14:30:15 - INFO - Processing: photo.webp -> photo.png
2025-11-27 14:30:15 - INFO - Loading image file: photo.webp (245,678 bytes)
2025-11-27 14:30:15 - INFO - Detected format: WEBP, dimensions: 4032x3024, mode: RGB, alpha: False
2025-11-27 14:30:16 - INFO - Successfully loaded image: 4032x3024 pixels, mode: RGB (0.85s)
2025-11-27 14:30:17 - INFO - Saved PNG file: photo.png (2,845,123 bytes)
...
2025-11-27 14:30:25 - INFO - Total conversion time: 10.23s
2025-11-27 14:30:25 - INFO - Elapsed time: 10.23s
2025-11-27 14:30:25 - INFO - Average time per file: 2.05s
```

## Troubleshooting

### "No supported image files found"
- Ensure your files are in the `images/source` folder
- Check that files have a supported extension: `.heic`, `.heif`, `.avif`, `.jpg`, `.jpeg`, `.png`, `.bmp`, `.tiff`, `.tif`, `.gif`, `.webp`, `.ico`, `.ppm`, `.pgm`, `.pbm`, `.tga` (or uppercase)
- Verify folder permissions

### "Required packages are not installed"
- Run `python setup.py` to install dependencies
- Or manually: `pip install -r requirements.txt`
- Check that you're using Python 3.7 or higher

### "Python is not installed or not in PATH"
- Install Python 3.7+ from [python.org](https://www.python.org)
- During installation, check "Add Python to PATH"
- Restart your terminal/command prompt after installation

### "Failed to convert" errors
- Check the log file in the `logs/` folder for detailed error messages
- Ensure image files are not corrupted
- Try converting one file at a time to isolate the problem
- Run with `-v` flag for more detailed debugging information
- For AVIF files: ensure pillow-heif was built with AVIF support

### Permission errors
- Ensure you have write permissions in the output directory
- Close any image viewers that might have output files open
- Run the script from a location where you have proper permissions

### Low quality output
- For JPG: Increase quality setting (e.g., `-q 95` or `-q 100`)
- For PNG: Already lossless, no quality setting needed
- For PDF: Try different page size if image appears too small/large

### Large file sizes
- Use JPG format with lower quality (e.g., `-q 85`) for smaller files
- PNG files are always lossless and will be larger
- PDF files include the full image data

## Tips

- **File naming**: Use descriptive names; the output will have the same base name
- **Batch processing**: The tool processes all image files at once - no need to convert one by one
- **Quality settings**: For JPG, quality 95 is near-lossless; 85 offers good balance; 70-80 is acceptable for web
- **Format selection**:
  - Use PNG for maximum quality and transparency
  - Use JPG for smallest files and web/email sharing
  - Use PDF for documents and printing
- **Keep originals**: The source files are never modified or deleted
- **Check logs**: Always review logs if something seems wrong

## Examples

### Example 1: Convert mixed-format photos to JPG for email
```bash
cd src
python convert_heic.py -f jpg -q 85
```

### Example 2: Convert to PDF documents with A4 pages
```bash
cd src
python convert_heic.py -f pdf --page-size a4
```

### Example 3: High-quality PNG for editing
```bash
cd src
python convert_heic.py -f png -v
```

### Example 4: Custom folders with verbose logging
```bash
cd src
python convert_heic.py -s ~/Pictures/Mixed -o ~/Pictures/Converted -f jpg -q 90 -v
```

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

This project is licensed under the terms specified in the LICENSE file.

## Acknowledgments

- Uses [pillow-heif](https://github.com/bigcat88/pillow_heif) for HEIC/HEIF/AVIF support
- Built with [Pillow (PIL)](https://python-pillow.org/) for image processing
- Uses [ReportLab](https://www.reportlab.com/) for PDF generation

## Support

If you encounter any issues:
1. Check the troubleshooting section above
2. Review the log files in the `logs/` folder
3. Run with `-v` flag for verbose output
4. Open an issue with your log file and error details
