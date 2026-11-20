#!/bin/bash

# SmartDrive Guardian AI - Setup and Run Script
# This script sets up the environment and runs the application

echo "======================================"
echo "SmartDrive Guardian AI - Setup"
echo "======================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.7+ from python.org"
    exit 1
fi

python3 --version

echo "[1/4] Python found, checking virtual environment..."

if [ ! -d "venv" ]; then
    echo "[2/4] Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to create virtual environment"
        exit 1
    fi
else
    echo "[2/4] Virtual environment already exists"
fi

echo "[3/4] Activating virtual environment and installing dependencies..."
source venv/bin/activate
pip install -r requirements.txt > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    echo "Running: pip install -r requirements.txt"
    pip install -r requirements.txt
    exit 1
fi

echo "[4/4] Launching SmartDrive Guardian AI..."
echo ""
echo "======================================"
echo "Application Starting..."
echo "======================================"
echo ""
echo "Close this window to stop the application"
echo ""

python3 smartdrive.py

echo ""
echo "Application closed."
