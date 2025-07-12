#!/bin/bash

# Dokemon API Setup Script for macOS/Linux
echo "Setting up Dokemon API..."

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed. Please install Python 3.6 or later."
    exit 1
fi

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "Installing requirements..."
pip install -r requirements.txt

echo ""
echo "Setup complete!"
echo ""
echo "To start the Dokemon API server:"
echo "1. Activate the virtual environment: source venv/bin/activate"
echo "2. Run the server: python app.py"
echo ""
echo "The API will be available at: http://localhost:9090"
