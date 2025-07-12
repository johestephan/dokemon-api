# Docker API Server Setup Script for Windows (PowerShell)
Write-Host "Setting up Docker API Server for Windows..." -ForegroundColor Green

# Check if Python is installed
try {
    $pythonVersion = python --version 2>$null
    Write-Host "Found Python: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "Error: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python from https://python.org" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Create virtual environment
Write-Host "Creating virtual environment..." -ForegroundColor Yellow
python -m venv venv

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& "venv\Scripts\Activate.ps1"

# Upgrade pip
Write-Host "Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip

# Install Flask
Write-Host "Installing Flask..." -ForegroundColor Yellow
pip install Flask==2.0.3

Write-Host ""
Write-Host "Setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "To run the Docker API server:" -ForegroundColor Cyan
Write-Host "1. Activate the virtual environment: venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host "2. Run the server: python app.py" -ForegroundColor White
Write-Host ""
Write-Host "The API will be available at: http://localhost:9090" -ForegroundColor Cyan

Read-Host "Press Enter to exit"
