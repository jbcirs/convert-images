#!/bin/bash
# Shell script to convert HEIC images
# This script runs from the scripts directory

echo "======================================"
echo "HEIC Image Converter Tool"
echo "======================================"
echo

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Navigate to src directory
cd "$SCRIPT_DIR/../src" || exit 1

# Check if convert_heic.py exists
if [ ! -f "convert_heic.py" ]; then
    echo "Error: convert_heic.py not found in src directory."
    echo "Please ensure the project structure is correct."
    echo
    read -p "Press Enter to exit..."
    exit 1
fi

# Check if Python is available
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo "Error: Python is not installed or not in PATH."
    echo "Please install Python 3.7 or higher."
    echo
    read -p "Press Enter to exit..."
    exit 1
fi

# Determine which Python command to use
PYTHON_CMD=""
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    # Check if python points to Python 3
    PYTHON_VERSION=$(python -c "import sys; print(sys.version_info.major)")
    if [ "$PYTHON_VERSION" = "3" ]; then
        PYTHON_CMD="python"
    else
        echo "Error: Python 3 is required, but 'python' points to Python 2."
        echo "Please install Python 3 or use 'python3' command."
        echo
        read -p "Press Enter to exit..."
        exit 1
    fi
fi

echo "Using Python command: $PYTHON_CMD"

# Check Python version
PYTHON_VERSION_FULL=$($PYTHON_CMD --version 2>&1)
echo "Python version: $PYTHON_VERSION_FULL"

# Check if required packages are installed
if ! $PYTHON_CMD -c "import pillow_heif" &> /dev/null; then
    echo
    echo "Required packages are not installed."
    echo "Running setup to install dependencies..."
    echo
    cd ..
    if ! $PYTHON_CMD setup.py; then
        echo
        echo "Setup failed. Please check the error messages above."
        echo
        read -p "Press Enter to exit..."
        exit 1
    fi
    cd src
    echo
    echo "Setup complete! Continuing with conversion..."
    echo
else
    echo "All required packages are installed."
fi

# Get user preferences
echo
echo "Select output format:"
echo "  1. PNG (default, lossless)"
echo "  2. JPG (smaller files)"
echo "  3. PDF (document format)"
echo
read -p "Enter choice (1-3, default=1): " FORMAT_CHOICE

if [ -z "$FORMAT_CHOICE" ]; then
    FORMAT_CHOICE=1
fi

case $FORMAT_CHOICE in
    1)
        OUTPUT_FORMAT="png"
        FORMAT_NAME="PNG"
        ;;
    2)
        OUTPUT_FORMAT="jpg"
        FORMAT_NAME="JPG"
        echo
        read -p "Enter JPG quality (1-100, default=95): " QUALITY
        if [ -z "$QUALITY" ]; then
            QUALITY=95
        fi
        ;;
    3)
        OUTPUT_FORMAT="pdf"
        FORMAT_NAME="PDF"
        echo
        echo "Select PDF page size:"
        echo "  1. Letter (default)"
        echo "  2. A4"
        read -p "Enter choice (1-2, default=1): " PAGE_CHOICE
        if [ "$PAGE_CHOICE" = "2" ]; then
            PAGE_SIZE="a4"
        else
            PAGE_SIZE="letter"
        fi
        ;;
    *)
        OUTPUT_FORMAT="png"
        FORMAT_NAME="PNG"
        ;;
esac

# Ask about verbose logging
echo
read -p "Enable verbose logging? (y/n, default=n): " VERBOSE

# Build command
CMD="$PYTHON_CMD convert_heic.py -f $OUTPUT_FORMAT"

if [ "$FORMAT_CHOICE" = "2" ] && [ ! -z "$QUALITY" ]; then
    CMD="$CMD -q $QUALITY"
fi

if [ "$FORMAT_CHOICE" = "3" ] && [ ! -z "$PAGE_SIZE" ]; then
    CMD="$CMD --page-size $PAGE_SIZE"
fi

if [[ "$VERBOSE" =~ ^[Yy]$ ]]; then
    CMD="$CMD -v"
fi

# Run the converter
echo
echo "======================================"
echo "Converting HEIC images to $FORMAT_NAME"
echo "======================================"
echo

$CMD

if [ $? -eq 0 ]; then
    echo
    echo "======================================"
    echo "Conversion completed successfully!"
    echo "======================================"
    echo
    echo "Output folder was cleared and new files added."
    echo "Check the output folder: ../images/output"
    echo "Check logs folder for details: ../logs"
else
    echo
    echo "======================================"
    echo "Conversion completed with errors."
    echo "======================================"
    echo
    echo "Output folder was cleared before conversion."
    echo "Please check the log files in ../logs for details."
fi

echo
read -p "Press Enter to exit..."
