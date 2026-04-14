@echo off
REM DXF Cleaner - Windows Batch File
REM Drag and drop a DXF file onto this to clean it

echo.
echo ===================================================================
echo DXF CLEANER - Drag and Drop
echo ===================================================================
echo.

if "%~1"=="" (
    echo No file provided!
    echo.
    echo Usage: Drag and drop a DXF file onto this batch file
    echo        or run: clean_dxf.bat "path\to\file.dxf"
    echo.
    pause
    exit /b 1
)

set INPUT_FILE=%~1
set OUTPUT_FILE=%~dpn1_CLEAN.dxf

echo Input:  %INPUT_FILE%
echo Output: %OUTPUT_FILE%
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo.
    echo Please install Python 3.8 or higher from python.org
    echo.
    pause
    exit /b 1
)

REM Check if ezdxf is installed
python -c "import ezdxf" >nul 2>&1
if errorlevel 1 (
    echo ERROR: ezdxf library is not installed
    echo.
    echo Installing ezdxf...
    python -m pip install ezdxf
    echo.
)

REM Run the cleaner
echo Cleaning file...
echo.
python "%~dp0dxf_cleaner.py" "%INPUT_FILE%" -o "%OUTPUT_FILE%"

echo.
echo ===================================================================
echo.
if errorlevel 1 (
    echo Cleaning FAILED!
) else (
    echo Cleaning COMPLETE!
    echo.
    echo Cleaned file: %OUTPUT_FILE%
)

echo.
pause
