# Dokemon API - Docker Start Script (PowerShell)
# This script starts the Dokemon API container

param(
    [string]$ImageName = "dokemon-ng/dokemon-api",
    [string]$Tag = "latest",
    [string]$ContainerName = "dokemon-api",
    [int]$HostPort = 9090,
    [int]$ContainerPort = 9090
)

Write-Host "🐳 Dokemon API - Docker Start Script" -ForegroundColor Cyan
Write-Host "====================================" -ForegroundColor Cyan

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

# Check if image exists
try {
    docker image inspect "$ImageName`:$Tag" | Out-Null
    if ($LASTEXITCODE -ne 0) {
        throw "Image not found"
    }
} catch {
    Write-Host "❌ Error: Docker image '$ImageName`:$Tag' not found" -ForegroundColor Red
    Write-Host "Please build the image first by running:" -ForegroundColor Yellow
    Write-Host "   .\docker-build.ps1" -ForegroundColor White
    Read-Host "Press Enter to exit"
    exit 1
}

# Stop and remove existing container if it exists
$existingContainer = docker ps -a --format "{{.Names}}" | Where-Object { $_ -eq $ContainerName }
if ($existingContainer) {
    Write-Host "🛑 Stopping existing container '$ContainerName'..." -ForegroundColor Yellow
    docker stop $ContainerName | Out-Null
    Write-Host "🗑️  Removing existing container '$ContainerName'..." -ForegroundColor Yellow
    docker rm $ContainerName | Out-Null
}

Write-Host "📋 Container Information:" -ForegroundColor Green
Write-Host "   Container Name: $ContainerName" -ForegroundColor White
Write-Host "   Image: $ImageName`:$Tag" -ForegroundColor White
Write-Host "   Port Mapping: $HostPort`:$ContainerPort" -ForegroundColor White
Write-Host ""

# Set default environment variables if not set
$secretKey = if ($env:SECRET_KEY) { $env:SECRET_KEY } else { "dokemon-change-this-secret-key" }
$adminPassword = if ($env:DEFAULT_ADMIN_PASSWORD) { $env:DEFAULT_ADMIN_PASSWORD } else { "admin" }

# Start the container
Write-Host "🚀 Starting Dokemon API container..." -ForegroundColor Yellow
$dockerArgs = @(
    "run", "-d",
    "--name", $ContainerName,
    "-p", "$HostPort`:$ContainerPort",
    "-u", "root",
    "-v", "/var/run/docker.sock:/var/run/docker.sock",
    "-v", "dokemon_data:/app/data",
    "-e", "SECRET_KEY=$secretKey",
    "-e", "DEFAULT_ADMIN_PASSWORD=$adminPassword",
    "--restart", "unless-stopped",
    "$ImageName`:$Tag"
)

& docker $dockerArgs

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✅ Container started successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "📊 Container Status:" -ForegroundColor Cyan
    docker ps --filter "name=$ContainerName"
    Write-Host ""
    Write-Host "🌐 API Access:" -ForegroundColor Green
    Write-Host "   Health Check: http://localhost:$HostPort/health" -ForegroundColor White
    Write-Host "   API Documentation: http://localhost:$HostPort/" -ForegroundColor White
    Write-Host "   Default Login: admin/admin (change immediately!)" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "📝 Useful Commands:" -ForegroundColor Cyan
    Write-Host "   View logs: docker logs -f $ContainerName" -ForegroundColor Gray
    Write-Host "   Stop container: docker stop $ContainerName" -ForegroundColor Gray
    Write-Host "   Remove container: docker rm $ContainerName" -ForegroundColor Gray
    Write-Host ""
    Write-Host "⚠️  Remember to change the default admin password!" -ForegroundColor Red
} else {
    Write-Host ""
    Write-Host "❌ Failed to start container!" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Read-Host "Press Enter to continue"
