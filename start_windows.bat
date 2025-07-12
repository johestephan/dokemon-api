@echo off
echo Starting Docker API Server...

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo Virtual environment not found. Please run setup_windows.bat first.
    pause
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Check if Docker is running
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Warning: Docker is not accessible. Make sure Docker Desktop is running.
    echo.
)

REM Start the API server
echo Starting Docker API Server on port 9090...
python app.py
