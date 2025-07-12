#!/bin/bash

# Start Dokemon API in production mode with Gunicorn
# Usage: ./start-prod.sh

set -e

echo "🚀 Starting Dokemon API in Production Mode"
echo "==========================================="

# Set production environment variables
export FLASK_ENV=production
export DOKEMON_DEBUG=false

# Check if Docker is running
if ! docker info >/dev/null 2>&1; then
    echo "❌ Error: Docker is not running or not accessible"
    echo "Please start Docker and ensure the socket is accessible"
    exit 1
fi

# Check if virtual environment should be activated
if [[ "$VIRTUAL_ENV" == "" ]] && [[ -f "venv/bin/activate" ]]; then
    echo "📦 Activating virtual environment..."
    source venv/bin/activate
fi

# Install/upgrade dependencies
echo "📦 Installing dependencies..."
pip install -r src/requirements.txt

# Show configuration
echo ""
echo "⚙️  Configuration:"
echo "   Host: ${DOKEMON_HOST:-0.0.0.0}"
echo "   Port: ${DOKEMON_PORT:-9090}"
echo "   Workers: ${GUNICORN_WORKERS:-auto}"
echo "   Environment: ${FLASK_ENV:-production}"
echo "   Debug: ${DOKEMON_DEBUG:-false}"
echo ""

# Start with Gunicorn
echo "🏃 Starting Gunicorn server..."
echo "API will be available at: http://${DOKEMON_HOST:-0.0.0.0}:${DOKEMON_PORT:-9090}"
echo "Press Ctrl+C to stop"
echo ""

# Add src to Python path and run Gunicorn
export PYTHONPATH="${PYTHONPATH}:./src"
exec gunicorn --config src/gunicorn.conf.py src.app:app
