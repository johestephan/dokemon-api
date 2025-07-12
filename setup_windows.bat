@echo off
echo Setting up Docker API Server for Windows...

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo Installing requirements...
pip install -r src\requirements.txt

echo.
echo Setup complete!
echo.
echo To run the Docker API server:
echo 1. Activate the virtual environment: venv\Scripts\activate.bat
echo 2. Run the server: cd src ^&^& python app.py
echo.
echo The API will be available at: http://localhost:9090
pause
