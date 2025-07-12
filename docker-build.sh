#!/bin/bash

# Dokemon API - Docker Build Script (Linux/macOS)
# This script builds the Docker image for the Dokemon API

set -e  # Exit on any error

echo "🐳 Dokemon API - Docker Build Script"
echo "====================================="

# Variables
IMAGE_NAME="dokemon-ng/dokemon-api"
TAG="latest"
BUILD_CONTEXT="."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Error: Docker is not running or not accessible"
    echo "Please start Docker and try again."
    exit 1
fi

echo "📋 Build Information:"
echo "   Image Name: $IMAGE_NAME:$TAG"
echo "   Build Context: $BUILD_CONTEXT"
echo ""

# Build the Docker image
echo "🔨 Building Docker image..."
docker build -t "$IMAGE_NAME:$TAG" "$BUILD_CONTEXT"

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Docker image built successfully!"
    echo ""
    echo "📊 Image Information:"
    docker images "$IMAGE_NAME:$TAG"
    echo ""
    echo "🚀 To start the container, run:"
    echo "   ./docker-start.sh"
    echo ""
    echo "   Or manually:"
    echo "   docker run -d -p 9090:9090 -v /var/run/docker.sock:/var/run/docker.sock $IMAGE_NAME:$TAG"
else
    echo ""
    echo "❌ Docker build failed!"
    exit 1
fi
