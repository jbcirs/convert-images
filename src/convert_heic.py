#!/usr/bin/env python3
"""
Image Converter Tool

Converts images between formats. Supported inputs: HEIC, HEIF, AVIF, JPG/JPEG,
PNG, BMP, TIFF/TIF, GIF (first frame), WebP, ICO, PPM, PGM, PBM, TGA.
Output formats: PDF, PNG, or JPG/JPEG.
Place image files in the images/source folder and they will be converted to the images/output folder.
"""

import os
import glob
import logging
import time
from pathlib import Path
from datetime import datetime
import argparse
import sys

try:
    from pillow_heif import register_heif_opener
    from PIL import Image
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.pdfgen import canvas
    from reportlab.lib.utils import ImageReader
except ImportError as e:
    print(f"Error: Required packages are not installed.")
    print(f"Missing: {e.name}")
    print("Please install all requirements using: pip install -r requirements.txt")
    print("Or run: python setup.py")
    sys.exit(1)

# Register HEIF opener with PIL
register_heif_opener()


def setup_logging(log_level=logging.INFO):
    """
    Setup logging configuration.
    
    Args:
        log_level: Logging level (default: INFO)
    """
    # Create logs directory if it doesn't exist
    script_dir = os.path.dirname(os.path.abspath(__file__))
    logs_dir = os.path.join(os.path.dirname(script_dir), 'logs')
    os.makedirs(logs_dir, exist_ok=True)
    
    # Create log file with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_file = os.path.join(logs_dir, f'convert_images_{timestamp}.log')
    
    # Configure logging to both file and console
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    logging.info(f"Log file created: {log_file}")
    return log_file


def clear_output_folder(output_folder, keep_readme=True):
    """
    Clear all converted files from the output folder.
    
    Args:
        output_folder (str): Path to the output folder
        keep_readme (bool): Whether to keep README.md file (default: True)
    """
    if not os.path.exists(output_folder):
        return
    
    extensions_to_remove = ['.png', '.jpg', '.jpeg', '.pdf', '.PNG', '.JPG', '.JPEG', '.PDF']
    removed_count = 0
    
    for filename in os.listdir(output_folder):
        filepath = os.path.join(output_folder, filename)
        
        # Skip directories and README files
        if os.path.isdir(filepath):
            continue
        if keep_readme and filename.lower() == 'readme.md':
            continue
        
        # Remove files with image/pdf extensions
        if any(filename.lower().endswith(ext.lower()) for ext in extensions_to_remove):
            try:
                os.remove(filepath)
                removed_count += 1
                logging.debug(f"Removed: {filename}")
            except Exception as e:
                logging.warning(f"Could not remove {filename}: {str(e)}")
    
    if removed_count > 0:
        logging.info(f"Cleared {removed_count} file(s) from output folder")
    else:
        logging.info("Output folder is already clean")


def get_image_files(source_folder):
    """
    Get all supported image files from the source folder.
    
    Args:
        source_folder (str): Path to the folder containing source image files
        
    Returns:
        list: List of image file paths sorted alphabetically
    """
    patterns = [
        '*.heic', '*.HEIC', '*.heif', '*.HEIF',        # HEIC/HEIF formats
        '*.avif', '*.AVIF',                              # AVIF format
        '*.jpg', '*.JPG', '*.jpeg', '*.JPEG',            # JPEG formats
        '*.png', '*.PNG',                                 # PNG formats
        '*.bmp', '*.BMP',                                 # BMP format
        '*.tiff', '*.TIFF', '*.tif', '*.TIF',            # TIFF formats
        '*.gif', '*.GIF',                                 # GIF format (first frame)
        '*.webp', '*.WEBP',                               # WebP format
        '*.ico', '*.ICO',                                 # ICO format
        '*.ppm', '*.PPM', '*.pgm', '*.PGM',              # PPM/PGM formats
        '*.pbm', '*.PBM',                                 # PBM format
        '*.tga', '*.TGA',                                 # TGA format
    ]
    image_files = []
    
    for pattern in patterns:
        image_pattern = os.path.join(source_folder, pattern)
        image_files.extend(glob.glob(image_pattern))
    
    return sorted(list(set(image_files)))  # Remove duplicates and sort


def convert_image_to_format(image_path, output_format='PNG', quality=95):
    """
    Convert image file to PIL Image object with metadata preservation.
    
    Args:
        image_path (str): Path to input image file (HEIC, JPG, or PNG)
        output_format (str): Output format (PNG or JPG)
        quality (int): Quality for JPG format (1-100)
        
    Returns:
        tuple: (PIL.Image, exif_data) or (None, None) if conversion fails
    """
    try:
        file_start = time.monotonic()
        input_size = os.path.getsize(image_path)
        logging.info(f"Loading image file: {os.path.basename(image_path)} ({input_size:,} bytes)")
        img = Image.open(image_path)

        detected_format = img.format or "unknown"
        has_alpha = img.mode in ('RGBA', 'LA', 'PA')
        logging.info(f"Detected format: {detected_format}, dimensions: {img.size[0]}x{img.size[1]}, mode: {img.mode}, alpha: {has_alpha}")

        # Extract EXIF data before any conversions
        exif_data = None
        try:
            exif_data = img.info.get('exif', None)
            if exif_data:
                logging.debug(f"Extracted EXIF metadata ({len(exif_data)} bytes)")
        except Exception as e:
            logging.debug(f"No EXIF data found or could not extract: {str(e)}")

        # Convert to RGB if necessary (required for JPG)
        if output_format.upper() == 'JPG' or output_format.upper() == 'JPEG':
            if img.mode in ('RGBA', 'LA', 'P'):
                # Create a white background
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
                img = background
            elif img.mode != 'RGB':
                img = img.convert('RGB')

        elapsed = time.monotonic() - file_start
        logging.info(f"Successfully loaded image: {img.size[0]}x{img.size[1]} pixels, mode: {img.mode} ({elapsed:.2f}s)")
        return img, exif_data

    except Exception as e:
        logging.error(f"Failed to convert {image_path}: {str(e)}")
        return None, None


def save_as_image(img, output_path, output_format='PNG', quality=95, exif_data=None):
    """
    Save PIL Image to file with metadata preservation.
    
    Args:
        img (PIL.Image): Image object to save
        output_path (str): Output file path
        output_format (str): Output format (PNG or JPG)
        quality (int): Quality for JPG format (1-100)
        exif_data: EXIF metadata to preserve (optional)
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        save_kwargs = {}
        
        if output_format.upper() in ['JPG', 'JPEG']:
            save_kwargs['format'] = 'JPEG'
            save_kwargs['quality'] = quality
            save_kwargs['optimize'] = True
            save_kwargs['subsampling'] = 0  # No subsampling for better quality
            save_kwargs['progressive'] = True  # Progressive JPG
            
            # Preserve EXIF data for JPG
            if exif_data:
                save_kwargs['exif'] = exif_data
        else:
            save_kwargs['format'] = 'PNG'
            save_kwargs['optimize'] = True
            save_kwargs['compress_level'] = 6  # Balanced compression (0-9)
            
            # PNG can store EXIF in 'exif' chunk
            if exif_data:
                save_kwargs['exif'] = exif_data
        
        img.save(output_path, **save_kwargs)
        
        file_size = os.path.getsize(output_path)
        logging.info(f"Saved {output_format} file: {os.path.basename(output_path)} ({file_size:,} bytes)")
        return True
        
    except Exception as e:
        logging.error(f"Failed to save {output_path}: {str(e)}")
        return False


def convert_image_to_pdf(image_path, output_path, page_size='LETTER'):
    """
    Convert image file to PDF format.
    
    Args:
        image_path (str): Path to input image file (HEIC, JPG, or PNG)
        output_path (str): Path for output PDF file
        page_size (str): Page size (LETTER or A4)
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        file_start = time.monotonic()
        logging.info(f"Converting to PDF: {os.path.basename(image_path)}")

        # Load the image
        img = Image.open(image_path)
        
        # Convert RGBA to RGB if necessary
        if img.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
            img = background
        elif img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Get image dimensions
        img_width, img_height = img.size
        
        # Set page size
        if page_size.upper() == 'A4':
            pdf_page_size = A4
        else:
            pdf_page_size = letter
        
        page_width, page_height = pdf_page_size
        
        # Calculate scaling to fit image on page while maintaining aspect ratio
        width_ratio = page_width / img_width
        height_ratio = page_height / img_height
        scale = min(width_ratio, height_ratio) * 0.9  # 90% of page to leave margins
        
        scaled_width = img_width * scale
        scaled_height = img_height * scale
        
        # Center the image on the page
        x_offset = (page_width - scaled_width) / 2
        y_offset = (page_height - scaled_height) / 2
        
        # Create PDF
        c = canvas.Canvas(output_path, pagesize=pdf_page_size)
        c.drawImage(ImageReader(img), x_offset, y_offset, scaled_width, scaled_height)
        c.save()
        
        file_size = os.path.getsize(output_path)
        elapsed = time.monotonic() - file_start
        logging.info(f"Saved PDF file: {os.path.basename(output_path)} ({file_size:,} bytes, {elapsed:.2f}s)")
        return True

    except Exception as e:
        logging.error(f"Failed to convert {image_path} to PDF: {str(e)}")
        return False


def convert_images(source_folder, output_folder, output_format='PNG', quality=95, page_size='LETTER', clear_output=True):
    """
    Convert all images from source folder to specified format in output folder.
    
    Args:
        source_folder (str): Path to folder containing image files (HEIC, JPG, PNG)
        output_folder (str): Path to folder for output files
        output_format (str): Output format (PDF, PNG, or JPG)
        quality (int): Quality for JPG format (1-100)
        page_size (str): Page size for PDF format (LETTER or A4)
        clear_output (bool): Clear output folder before conversion (default: True)
        
    Returns:
        dict: Statistics about conversion results
    """
    # Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)
    logging.info(f"Output folder: {output_folder}")
    
    # Clear output folder if requested
    if clear_output:
        clear_output_folder(output_folder)
    
    # Get all image files
    image_files = get_image_files(source_folder)
    
    if not image_files:
        logging.warning(f"No supported image files found in {source_folder}")
        return {'total': 0, 'successful': 0, 'failed': 0, 'elapsed_seconds': 0.0}

    logging.info(f"Found {len(image_files)} image file(s) to convert")

    # Convert each file
    total_start = time.monotonic()
    successful = 0
    failed = 0

    for image_file in image_files:
        filename = os.path.basename(image_file)
        base_name = os.path.splitext(filename)[0]
        
        # Determine output file extension
        if output_format.upper() == 'PDF':
            output_ext = '.pdf'
        elif output_format.upper() in ['JPG', 'JPEG']:
            output_ext = '.jpg'
        else:
            output_ext = '.png'
        
        output_path = os.path.join(output_folder, f"{base_name}{output_ext}")
        
        logging.info(f"Processing: {filename} -> {os.path.basename(output_path)}")
        
        # Convert based on format
        if output_format.upper() == 'PDF':
            success = convert_image_to_pdf(image_file, output_path, page_size)
        else:
            img, exif_data = convert_image_to_format(image_file, output_format, quality)
            if img:
                success = save_as_image(img, output_path, output_format, quality, exif_data)
            else:
                success = False
        
        if success:
            successful += 1
        else:
            failed += 1
    
    total_elapsed = time.monotonic() - total_start
    logging.info(f"Total conversion time: {total_elapsed:.2f}s")

    return {
        'total': len(image_files),
        'successful': successful,
        'failed': failed,
        'elapsed_seconds': total_elapsed
    }


def main():
    """Main function to handle command line arguments and execute conversion."""
    parser = argparse.ArgumentParser(
        description=(
            "Convert images to PDF, PNG, or JPG format.\n"
            "Supported inputs: HEIC, HEIF, AVIF, JPG/JPEG, PNG, BMP, TIFF/TIF,\n"
            "GIF (first frame), WebP, ICO, PPM, PGM, PBM, TGA."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python convert_heic.py                           # Convert to PNG (default)
  python convert_heic.py -f jpg                    # Convert to JPG
  python convert_heic.py -f pdf                    # Convert to PDF
  python convert_heic.py -f jpg -q 90              # Convert to JPG with 90% quality
  python convert_heic.py -s /path/to/images        # Specify source folder
  python convert_heic.py -o /path/to/output        # Specify output folder
  python convert_heic.py -f pdf --page-size A4     # Convert to PDF with A4 page size
  python convert_heic.py -v                        # Enable verbose logging
        """
    )
    
    # Default paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    default_source = os.path.join(project_root, 'images', 'source')
    default_output = os.path.join(project_root, 'images', 'output')
    
    parser.add_argument(
        '-s', '--source',
        default=default_source,
        help=f'Source folder containing image files (default: {default_source})'
    )
    
    parser.add_argument(
        '-o', '--output',
        default=default_output,
        help=f'Output folder for converted files (default: {default_output})'
    )
    
    parser.add_argument(
        '-f', '--format',
        choices=['pdf', 'png', 'jpg', 'jpeg', 'PDF', 'PNG', 'JPG', 'JPEG'],
        default='png',
        help='Output format (default: png)'
    )
    
    parser.add_argument(
        '-q', '--quality',
        type=int,
        default=95,
        help='Quality for JPG format, 1-100 (default: 95)'
    )
    
    parser.add_argument(
        '--page-size',
        choices=['letter', 'a4', 'LETTER', 'A4'],
        default='letter',
        help='Page size for PDF format (default: letter)'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose logging (DEBUG level)'
    )
    
    parser.add_argument(
        '--no-clear',
        action='store_true',
        help='Do not clear output folder before conversion (default: clear output folder)'
    )
    
    args = parser.parse_args()
    
    # Setup logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    log_file = setup_logging(log_level)
    
    # Validate quality parameter
    if args.quality < 1 or args.quality > 100:
        logging.error("Quality must be between 1 and 100")
        sys.exit(1)
    
    # Check if source folder exists
    if not os.path.exists(args.source):
        logging.error(f"Source folder does not exist: {args.source}")
        sys.exit(1)
    
    if not os.path.isdir(args.source):
        logging.error(f"Source path is not a directory: {args.source}")
        sys.exit(1)
    
    # Log configuration
    logging.info("=" * 60)
    logging.info("Image Converter")
    logging.info("=" * 60)
    logging.info(f"Source folder: {args.source}")
    logging.info(f"Output folder: {args.output}")
    logging.info(f"Output format: {args.format.upper()}")
    if args.format.upper() in ['JPG', 'JPEG']:
        logging.info(f"JPG Quality: {args.quality}%")
    if args.format.upper() == 'PDF':
        logging.info(f"PDF Page size: {args.page_size.upper()}")
    logging.info("=" * 60)
    
    try:
        # Perform conversion
        stats = convert_images(
            args.source,
            args.output,
            args.format,
            args.quality,
            args.page_size,
            clear_output=not args.no_clear
        )
        
        # Print summary
        logging.info("=" * 60)
        logging.info("Conversion Summary")
        logging.info("=" * 60)
        logging.info(f"Total files found: {stats['total']}")
        logging.info(f"Successfully converted: {stats['successful']}")
        logging.info(f"Failed conversions: {stats['failed']}")
        
        if stats['total'] > 0:
            success_rate = (stats['successful'] / stats['total']) * 100
            logging.info(f"Success rate: {success_rate:.1f}%")
            elapsed = stats.get('elapsed_seconds', 0.0)
            logging.info(f"Elapsed time: {elapsed:.2f}s")
            if stats['successful'] > 0:
                avg_time = elapsed / stats['successful']
                logging.info(f"Average time per file: {avg_time:.2f}s")
        
        logging.info("=" * 60)
        logging.info(f"Check output folder: {args.output}")
        logging.info(f"Log file: {log_file}")
        
        if stats['failed'] > 0:
            sys.exit(1)
        
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        import traceback
        logging.debug(traceback.format_exc())
        sys.exit(1)


if __name__ == "__main__":
    main()
