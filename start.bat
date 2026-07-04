@echo off
title Book Fabric Launcher
echo ==========================================
echo    🚀 Launching BOOK FABRIC...
echo ==========================================
echo.

:: Check if python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH.
    echo Please install Python from python.org first.
    pause
    exit /b
)

echo [1/2] Checking dependencies...
pip install -r requirements.txt --quiet

echo [2/2] Starting the application...
:: Set PYTHONPATH to the current directory so Python can find the book_fabric package
set PYTHONPATH=%CD%
streamlit run book_fabric/ui/streamlit_app.py

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] The application failed to start.
    pause
)
