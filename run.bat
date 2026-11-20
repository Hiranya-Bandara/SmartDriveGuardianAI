@echo off
REM SmartDrive Guardian AI - Setup and Run Script
REM This script sets up the environment and runs the application

echo ======================================
echo SmartDrive Guardian AI - Setup
echo ======================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7+ from python.org
    pause
    exit /b 1
)

echo [1/4] Python found, checking virtual environment...
if not exist "venv" (
    echo [2/4] Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
) else (
    echo [2/4] Virtual environment already exists
)

echo [3/4] Activating virtual environment and installing dependencies...
call venv\Scripts\activate.bat
pip install -r requirements.txt >nul 2>&1
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    echo Running: pip install -r requirements.txt
    pip install -r requirements.txt
    pause
    exit /b 1
)

echo [4/4] Launching SmartDrive Guardian AI...
echo.
echo ======================================
echo Application Starting...
echo ======================================
echo.
echo Close this window to stop the application
echo.

python smartdrive.py

echo.
echo Application closed.
pause
