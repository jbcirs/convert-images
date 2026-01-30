#!/usr/bin/env python3
"""
Setup script for Image Converter Tool

This script helps set up the environment and install dependencies.
"""

import subprocess
import sys
import os

def install_package(package_name):
    """Install a package using pip."""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error installing {package_name}: {e}")
        return False

def check_python_version():
    """Check if Python version is compatible."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print(f"Error: Python 3.7 or higher is required. You have Python {version.major}.{version.minor}")
        return False
    print(f"✓ Python {version.major}.{version.minor}.{version.micro} is compatible")
    return True

def check_dependencies():
    """Check if required dependencies are installed."""
    required_packages = [
        ('pillow-heif', 'pillow_heif'),
        ('Pillow', 'PIL'),
        ('reportlab', 'reportlab')
    ]
    
    missing_packages = []
    
    for package_name, import_name in required_packages:
        try:
            __import__(import_name)
            print(f"✓ {package_name} is already installed")
        except ImportError:
            print(f"✗ {package_name} is not installed")
            missing_packages.append(package_name)
    
    return len(missing_packages) == 0, missing_packages

def setup_directories():
    """Ensure required directories exist."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    directories = [
        os.path.join(script_dir, "images", "source"),
        os.path.join(script_dir, "images", "output"),
        os.path.join(script_dir, "logs")
    ]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✓ Created directory: {directory}")
        else:
            print(f"✓ Directory exists: {directory}")
    
    return True

def create_readme_files():
    """Create README files in the images subdirectories if they don't exist."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Source folder README
    source_readme = os.path.join(script_dir, "images", "source", "README.md")
    if not os.path.exists(source_readme):
        with open(source_readme, 'w') as f:
            f.write("# Source Images Folder\n\n")
            f.write("Place your image files in this folder.\n\n")
            f.write("Supported input formats:\n")
            f.write("- HEIC/HEIF (.heic, .heif)\n")
            f.write("- AVIF (.avif)\n")
            f.write("- JPEG (.jpg, .jpeg)\n")
            f.write("- PNG (.png)\n")
            f.write("- BMP (.bmp)\n")
            f.write("- TIFF (.tiff, .tif)\n")
            f.write("- GIF (.gif) - first frame only\n")
            f.write("- WebP (.webp)\n")
            f.write("- ICO (.ico)\n")
            f.write("- PPM/PGM/PBM (.ppm, .pgm, .pbm)\n")
            f.write("- TGA (.tga)\n\n")
            f.write("The converter will automatically detect and process all supported image files in this folder.\n")
        print(f"✓ Created {source_readme}")
    else:
        print(f"✓ README exists: {source_readme}")
    
    # Output folder README
    output_readme = os.path.join(script_dir, "images", "output", "README.md")
    if not os.path.exists(output_readme):
        with open(output_readme, 'w') as f:
            f.write("# Output Images Folder\n\n")
            f.write("Converted images will be saved in this folder.\n\n")
            f.write("The output format depends on the conversion option you choose:\n")
            f.write("- PDF format (.pdf)\n")
            f.write("- PNG format (.png)\n")
            f.write("- JPG format (.jpg)\n\n")
            f.write("Output files will have the same base name as the source files.\n")
        print(f"✓ Created {output_readme}")
    else:
        print(f"✓ README exists: {output_readme}")

def main():
    """Run the setup process."""
    print("=" * 60)
    print("Image Converter Tool - Setup")
    print("=" * 60)
    print()
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    print()
    
    # Check dependencies
    dependencies_ok, missing_packages = check_dependencies()
    
    if not dependencies_ok:
        print("\n" + "=" * 60)
        print("Installing missing dependencies...")
        print("=" * 60)
        
        for package in missing_packages:
            print(f"\nInstalling {package}...")
            if install_package(package):
                print(f"✓ {package} installed successfully")
            else:
                print(f"✗ Failed to install {package}")
                print("Please try installing manually: pip install -r requirements.txt")
                sys.exit(1)
    
    print("\n" + "=" * 60)
    print("Setting up directories...")
    print("=" * 60)
    
    # Setup directories
    setup_directories()
    
    # Create README files
    print()
    create_readme_files()
    
    print("\n" + "=" * 60)
    print("Setup Complete!")
    print("=" * 60)
    print("\nThe Image Converter Tool is ready to use!")
    print("\nNext steps:")
    print("1. Add image files to the 'images/source' folder")
    print("2. Navigate to src: cd src")
    print("3. Run the converter:")
    print("   - Convert to PNG:  python convert_heic.py")
    print("   - Convert to JPG:  python convert_heic.py -f jpg")
    print("   - Convert to PDF:  python convert_heic.py -f pdf")
    print("4. Check the output in 'images/output' folder")
    print("5. Review logs in 'logs' folder for debugging")
    print("\nFor help, run: python convert_heic.py --help")
    print("\nQuick start scripts:")
    print("  Windows: cd src && .\\convert_heic.bat")
    print("  Unix/Mac: cd src && ./convert_heic.sh")

if __name__ == "__main__":
    main()
