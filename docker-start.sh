#!/bin/bash

# Dokemon API - Docker Start Script (Linux/macOS)
# This script starts the Dokemon API container

set -e  # Exit on any error

echo "🐳 Dokemon API - Docker Start Script"
echo "===================================="

# Variables
IMAGE_NAME="dokemon-ng/dokemon-api"
TAG="latest"
CONTAINER_NAME="dokemon-api"
HOST_PORT="9090"
CONTAINER_PORT="9090"

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Error: Docker is not running or not accessible"
    echo "Please start Docker and try again."
    exit 1
fi

# Check if image exists
if ! docker image inspect "$IMAGE_NAME:$TAG" > /dev/null 2>&1; then
    echo "❌ Error: Docker image '$IMAGE_NAME:$TAG' not found"
    echo "Please build the image first by running:"
    echo "   ./docker-build.sh"
    exit 1
fi

# Stop and remove existing container if it exists
if docker ps -a --format "table {{.Names}}" | grep -q "^$CONTAINER_NAME$"; then
    echo "🛑 Stopping existing container '$CONTAINER_NAME'..."
    docker stop "$CONTAINER_NAME" > /dev/null 2>&1 || true
    echo "🗑️  Removing existing container '$CONTAINER_NAME'..."
    docker rm "$CONTAINER_NAME" > /dev/null 2>&1 || true
fi

echo "📋 Container Information:"
echo "   Container Name: $CONTAINER_NAME"
echo "   Image: $IMAGE_NAME:$TAG"
echo "   Port Mapping: $HOST_PORT:$CONTAINER_PORT"
echo ""

# Start the container
echo "🚀 Starting Dokemon API container..."
docker run -d \
    --name "$CONTAINER_NAME" \
    -p "$HOST_PORT:$CONTAINER_PORT" \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -v dokemon_data:/app/data \
    -e SECRET_KEY="${SECRET_KEY:-dokemon-change-this-secret-key}" \
    -e DEFAULT_ADMIN_PASSWORD="${DEFAULT_ADMIN_PASSWORD:-admin}" \
    --restart unless-stopped \
    "$IMAGE_NAME:$TAG"

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Container started successfully!"
    echo ""
    echo "📊 Container Status:"
    docker ps --filter "name=$CONTAINER_NAME"
    echo ""
    echo "🌐 API Access:"
    echo "   Health Check: http://localhost:$HOST_PORT/health"
    echo "   API Documentation: http://localhost:$HOST_PORT/"
    echo "   Default Login: admin/admin (change immediately!)"
    echo ""
    echo "📝 Useful Commands:"
    echo "   View logs: docker logs -f $CONTAINER_NAME"
    echo "   Stop container: docker stop $CONTAINER_NAME"
    echo "   Remove container: docker rm $CONTAINER_NAME"
    echo ""
    echo "⚠️  Remember to change the default admin password!"
else
    echo ""
    echo "❌ Failed to start container!"
    exit 1
fi
