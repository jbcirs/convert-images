@echo off
setlocal enabledelayedexpansion
REM Windows batch script to convert HEIC images
REM This script runs from the scripts directory

echo ======================================
echo Image Converter Tool
echo ======================================
echo.

REM Navigate to src directory where Python script is located
cd /d "%~dp0..\src"

REM Check if convert_heic.py exists
if not exist "convert_heic.py" (
    echo Error: convert_heic.py not found in src directory.
    echo Please ensure the project structure is correct.
    echo.
    pause
    exit /b 1
)

REM Check if Python is available
python --version >nul 2>&1
if !errorlevel! neq 0 (
    echo Error: Python is not installed or not in PATH.
    echo Please install Python 3.7 or higher.
    echo.
    pause
    exit /b 1
)

REM Check Python version
for /f "tokens=2 delims= " %%a in ('python --version 2^>^&1') do set PYTHON_VERSION=%%a
echo Found Python version: %PYTHON_VERSION%

REM Check if required packages are installed
python -c "import pillow_heif" >nul 2>&1
if !errorlevel! neq 0 (
    echo.
    echo Required packages are not installed.
    echo Running setup to install dependencies...
    echo.
    cd ..
    python setup.py
    set SETUP_RESULT=!errorlevel!
    cd src
    if !SETUP_RESULT! neq 0 (
        echo.
        echo Setup failed. Please check the error messages above.
        echo.
        pause
        exit /b 1
    )
    echo.
    echo Setup complete! Continuing with conversion...
    echo.
) else (
    echo All required packages are installed.
)

REM Get user preferences
echo.
echo Select output format:
echo   1. PNG (default, lossless)
echo   2. JPG (smaller files)
echo   3. PDF (document format)
echo.
set /p FORMAT_CHOICE="Enter choice (1-3, default=1): "

if "%FORMAT_CHOICE%"=="" set FORMAT_CHOICE=1

if "%FORMAT_CHOICE%"=="1" (
    set OUTPUT_FORMAT=png
    set FORMAT_NAME=PNG
)
if "%FORMAT_CHOICE%"=="2" (
    set OUTPUT_FORMAT=jpg
    set FORMAT_NAME=JPG
    echo.
    set /p QUALITY="Enter JPG quality (1-100, default=95): "
    if "!QUALITY!"=="" set QUALITY=95
)
if "%FORMAT_CHOICE%"=="3" (
    set OUTPUT_FORMAT=pdf
    set FORMAT_NAME=PDF
    echo.
    echo Select PDF page size:
    echo   1. Letter (default)
    echo   2. A4
    set /p PAGE_CHOICE="Enter choice (1-2, default=1): "
    if "!PAGE_CHOICE!"=="2" (
        set PAGE_SIZE=a4
    ) else (
        set PAGE_SIZE=letter
    )
)

REM Ask about verbose logging
echo.
set /p VERBOSE="Enable verbose logging? (y/n, default=n): "

REM Build command
set CMD=python convert_heic.py -f %OUTPUT_FORMAT%

if "%FORMAT_CHOICE%"=="2" (
    if not "!QUALITY!"=="" (
        set CMD=!CMD! -q !QUALITY!
    )
)

if "%FORMAT_CHOICE%"=="3" (
    if not "!PAGE_SIZE!"=="" (
        set CMD=!CMD! --page-size !PAGE_SIZE!
    )
)

if /i "%VERBOSE%"=="y" (
    set CMD=!CMD! -v
)

REM Run the converter
echo.
echo ======================================
echo Converting images to %FORMAT_NAME%
echo ======================================
echo.

!CMD!

echo.
if !errorlevel! equ 0 (
    echo ======================================
    echo Conversion completed successfully!
    echo ======================================
    echo.
    echo Check the output folder: ..\images\output
    echo Check logs folder for details: ..\logs
    echo.
    echo Note: Output folder was cleared before conversion.
) else (
    echo ======================================
    echo Conversion completed with errors.
    echo ======================================
    echo.
    echo Please check the log files in ..\logs for details.
    echo.
    echo Note: Output folder was cleared before conversion.
)

echo.
pause
