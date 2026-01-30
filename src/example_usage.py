#!/usr/bin/env python3
"""
Example Usage of Image Converter

This script demonstrates how to use the convert_heic module programmatically.
"""

import os
import sys

# Add the src directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from convert_heic import (
    convert_images,
    convert_image_to_format,
    convert_image_to_pdf,
    save_as_image,
    get_image_files,
    setup_logging
)


def example_1_basic_conversion():
    """Example 1: Basic conversion to PNG (simplest usage)"""
    print("=" * 60)
    print("Example 1: Basic conversion to PNG")
    print("=" * 60)
    
    # Setup logging
    setup_logging()
    
    # Get the project root directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    
    source_folder = os.path.join(project_root, 'images', 'source')
    output_folder = os.path.join(project_root, 'images', 'output')
    
    # Convert all image files to PNG
    stats = convert_images(
        source_folder=source_folder,
        output_folder=output_folder,
        output_format='PNG'
    )
    
    print(f"\nResults: {stats['successful']}/{stats['total']} files converted successfully")
    print()


def example_2_jpg_with_quality():
    """Example 2: Convert to JPG with custom quality"""
    print("=" * 60)
    print("Example 2: Convert to JPG with 85% quality")
    print("=" * 60)
    
    # Setup logging
    setup_logging()
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    
    source_folder = os.path.join(project_root, 'images', 'source')
    output_folder = os.path.join(project_root, 'images', 'output')
    
    # Convert to JPG with 85% quality
    stats = convert_images(
        source_folder=source_folder,
        output_folder=output_folder,
        output_format='JPG',
        quality=85
    )
    
    print(f"\nResults: {stats['successful']}/{stats['total']} files converted successfully")
    print()


def example_3_pdf_a4():
    """Example 3: Convert to PDF with A4 page size"""
    print("=" * 60)
    print("Example 3: Convert to PDF with A4 page size")
    print("=" * 60)
    
    # Setup logging
    setup_logging()
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    
    source_folder = os.path.join(project_root, 'images', 'source')
    output_folder = os.path.join(project_root, 'images', 'output')
    
    # Convert to PDF with A4 page size
    stats = convert_images(
        source_folder=source_folder,
        output_folder=output_folder,
        output_format='PDF',
        page_size='A4'
    )
    
    print(f"\nResults: {stats['successful']}/{stats['total']} files converted successfully")
    print()


def example_4_single_file():
    """Example 4: Convert a single specific file"""
    print("=" * 60)
    print("Example 4: Convert a single specific file")
    print("=" * 60)
    
    # Setup logging
    setup_logging()
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    
    source_folder = os.path.join(project_root, 'images', 'source')
    output_folder = os.path.join(project_root, 'images', 'output')
    
    # Get all image files
    image_files = get_image_files(source_folder)

    if not image_files:
        print("No supported image files found in source folder")
        return

    # Convert just the first file to PNG
    image_file = image_files[0]
    filename = os.path.basename(image_file)
    base_name = os.path.splitext(filename)[0]

    print(f"Converting: {filename}")

    # Convert to image with metadata
    img, exif_data = convert_image_to_format(image_file, output_format='PNG')
    
    if img:
        output_path = os.path.join(output_folder, f"{base_name}.png")
        success = save_as_image(img, output_path, output_format='PNG', exif_data=exif_data)
        
        if success:
            print(f"Successfully converted to: {output_path}")
            if exif_data:
                print(f"EXIF metadata preserved ({len(exif_data)} bytes)")
        else:
            print("Failed to save image")
    else:
        print("Failed to convert image")
    
    print()


def example_5_custom_folders():
    """Example 5: Use custom source and output folders"""
    print("=" * 60)
    print("Example 5: Use custom source and output folders")
    print("=" * 60)
    
    # Setup logging
    setup_logging()
    
    # Custom folder paths (modify these as needed)
    source_folder = r"C:\Users\YourName\Pictures\iPhone"
    output_folder = r"C:\Users\YourName\Pictures\Converted"
    
    # Check if custom folders exist
    if not os.path.exists(source_folder):
        print(f"Source folder does not exist: {source_folder}")
        print("Please modify the paths in this example to match your system")
        return
    
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    # Convert to JPG
    stats = convert_images(
        source_folder=source_folder,
        output_folder=output_folder,
        output_format='JPG',
        quality=90
    )
    
    print(f"\nResults: {stats['successful']}/{stats['total']} files converted successfully")
    print()


def example_6_batch_processing():
    """Example 6: Process files and collect information"""
    print("=" * 60)
    print("Example 6: Batch processing with file information")
    print("=" * 60)
    
    # Setup logging
    setup_logging()
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    
    source_folder = os.path.join(project_root, 'images', 'source')
    output_folder = os.path.join(project_root, 'images', 'output')
    
    # Get all image files
    image_files = get_image_files(source_folder)

    if not image_files:
        print("No supported image files found in source folder")
        return

    print(f"Found {len(image_files)} image file(s):\n")

    results = []

    for image_file in image_files:
        filename = os.path.basename(image_file)
        base_name = os.path.splitext(filename)[0]

        # Get file size
        file_size = os.path.getsize(image_file)

        # Convert to JPG with metadata
        img, exif_data = convert_image_to_format(image_file, output_format='JPG', quality=90)
        
        if img:
            output_path = os.path.join(output_folder, f"{base_name}.jpg")
            success = save_as_image(img, output_path, output_format='JPG', quality=90, exif_data=exif_data)
            
            if success:
                output_size = os.path.getsize(output_path)
                compression_ratio = (1 - output_size / file_size) * 100
                
                results.append({
                    'filename': filename,
                    'original_size': file_size,
                    'output_size': output_size,
                    'compression_ratio': compression_ratio,
                    'success': True
                })
            else:
                results.append({
                    'filename': filename,
                    'success': False
                })
        else:
            results.append({
                'filename': filename,
                'success': False
            })
    
    # Print summary
    print("\nConversion Summary:")
    print("-" * 80)
    print(f"{'Filename':<30} {'Original':<15} {'Output':<15} {'Compression':<15}")
    print("-" * 80)
    
    for result in results:
        if result['success']:
            orig_mb = result['original_size'] / (1024 * 1024)
            out_mb = result['output_size'] / (1024 * 1024)
            comp_pct = result['compression_ratio']
            print(f"{result['filename']:<30} {orig_mb:>10.2f} MB  {out_mb:>10.2f} MB  {comp_pct:>10.1f}%")
        else:
            print(f"{result['filename']:<30} {'FAILED':<15}")
    
    print("-" * 80)
    successful = sum(1 for r in results if r['success'])
    print(f"Total: {successful}/{len(results)} files converted successfully")
    print()


def main():
    """Run all examples"""
    print("\n" + "=" * 60)
    print("Image Converter - Usage Examples")
    print("=" * 60)
    print("\nThis script demonstrates various ways to use the converter.\n")
    
    # Display menu
    print("Available examples:")
    print("  1. Basic conversion to PNG")
    print("  2. Convert to JPG with custom quality")
    print("  3. Convert to PDF with A4 page size")
    print("  4. Convert a single specific file")
    print("  5. Use custom source and output folders")
    print("  6. Batch processing with file information")
    print("  0. Run all examples")
    print()
    
    choice = input("Enter example number to run (0-6): ").strip()
    
    if choice == '1':
        example_1_basic_conversion()
    elif choice == '2':
        example_2_jpg_with_quality()
    elif choice == '3':
        example_3_pdf_a4()
    elif choice == '4':
        example_4_single_file()
    elif choice == '5':
        example_5_custom_folders()
    elif choice == '6':
        example_6_batch_processing()
    elif choice == '0':
        example_1_basic_conversion()
        example_2_jpg_with_quality()
        example_3_pdf_a4()
        example_4_single_file()
        example_6_batch_processing()
        print("Note: Example 5 requires custom folder paths - run separately")
    else:
        print("Invalid choice. Please run again and select 0-6.")


if __name__ == "__main__":
    main()
