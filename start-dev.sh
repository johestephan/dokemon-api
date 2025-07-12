#!/bin/bash

# Start Dokemon API in development mode with Flask's built-in server
# Usage: ./start-dev.sh

set -e

echo "🔧 Starting Dokemon API in Development Mode"
echo "============================================"

# Set development environment variables
export FLASK_ENV=development
export DOKEMON_DEBUG=true

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
pip install -r requirements.txt

# Show configuration
echo ""
echo "⚙️  Configuration:"
echo "   Host: ${DOKEMON_HOST:-0.0.0.0}"
echo "   Port: ${DOKEMON_PORT:-9090}"
echo "   Environment: ${FLASK_ENV:-development}"
echo "   Debug: ${DOKEMON_DEBUG:-true}"
echo ""

# Start with Flask development server
echo "🏃 Starting Flask development server..."
echo "API will be available at: http://${DOKEMON_HOST:-0.0.0.0}:${DOKEMON_PORT:-9090}"
echo "Press Ctrl+C to stop"
echo ""

exec python app.py
