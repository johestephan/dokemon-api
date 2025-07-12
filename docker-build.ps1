# Dokemon API - Docker Build Script (PowerShell)
# This script builds the Docker image for the Dokemon API

param(
    [string]$ImageName = "dokemon-ng/dokemon-api",
    [string]$Tag = "latest",
    [string]$BuildContext = "."
)

Write-Host "🐳 Dokemon API - Docker Build Script" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan

# Check if Docker is running
try {
    docker info | Out-Null
    if ($LASTEXITCODE -ne 0) {
        throw "Docker command failed"
    }
} catch {
    Write-Host "❌ Error: Docker is not running or not accessible" -ForegroundColor Red
    Write-Host "Please start Docker Desktop and try again." -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "📋 Build Information:" -ForegroundColor Green
Write-Host "   Image Name: $ImageName`:$Tag" -ForegroundColor White
Write-Host "   Build Context: $BuildContext" -ForegroundColor White
Write-Host ""

# Build the Docker image
Write-Host "🔨 Building Docker image..." -ForegroundColor Yellow
docker build -t "$ImageName`:$Tag" $BuildContext

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✅ Docker image built successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "📊 Image Information:" -ForegroundColor Cyan
    docker images "$ImageName`:$Tag"
    Write-Host ""
    Write-Host "🚀 To start the container, run:" -ForegroundColor Green
    Write-Host "   .\docker-start.ps1" -ForegroundColor White
    Write-Host ""
    Write-Host "   Or manually:" -ForegroundColor Gray
    Write-Host "   docker run -d -p 9090:9090 -v /var/run/docker.sock:/var/run/docker.sock $ImageName`:$Tag" -ForegroundColor Gray
} else {
    Write-Host ""
    Write-Host "❌ Docker build failed!" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Read-Host "Press Enter to continue"
