# Source Images Folder

Place your image files in this folder to convert them.

## Supported Input Formats

| Category | Extensions |
|----------|------------|
| **HEIC/HEIF** | `.heic`, `.heif` |
| **AVIF** | `.avif` |
| **JPEG** | `.jpg`, `.jpeg` |
| **PNG** | `.png` |
| **BMP** | `.bmp` |
| **TIFF** | `.tiff`, `.tif` |
| **GIF** | `.gif` (first frame only) |
| **WebP** | `.webp` (first frame for animated) |
| **ICO** | `.ico` (largest size) |
| **Netpbm** | `.ppm`, `.pgm`, `.pbm` |
| **TGA** | `.tga` |

Both lowercase and uppercase extensions are accepted.

## Instructions

1. **Copy your image files** into this folder
2. **Run the converter** using one of these methods:
   - Windows: `cd scripts` then `.\convert_heic.bat`
   - Unix/Mac: `cd scripts` then `./convert_heic.sh`
   - Command line: `python src/convert_heic.py -f [format]`
3. **Check the output** in the `../output` folder

## Tips

- You can add multiple files at once - the converter processes them all in one go
- File names are preserved (only the extension changes)
- Original files are never modified or deleted
- Subfolders are not scanned - only files directly in this folder

## Example

If you add these files:
```
source/
├── IMG_1234.heic
├── photo.webp
├── scan.tiff
├── icon.bmp
└── vacation.png
```

After conversion (to JPG), you'll get:
```
output/
├── IMG_1234.jpg
├── photo.jpg
├── scan.jpg
├── icon.jpg
└── vacation.jpg
```

Need help? Check the main README.md in the project root.
