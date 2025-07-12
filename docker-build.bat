@echo off
REM Dokemon API - Docker Build Script (Windows)
REM This script builds the Docker image for the Dokemon API

setlocal EnableDelayedExpansion

echo [*] Dokemon API - Docker Build Script
echo =====================================

REM Variables
set IMAGE_NAME=javastraat/dokemon-api
set TAG=latest
set BUILD_CONTEXT=.

REM Check if Docker is running
docker info >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [X] Error: Docker is not running or not accessible
    echo Please start Docker Desktop and try again.
    pause
    exit /b 1
)

echo [i] Build Information:
echo    Image Name: %IMAGE_NAME%:%TAG%
echo    Build Context: %BUILD_CONTEXT%
echo.

REM Build the Docker image
echo [+] Building Docker image...
docker build -t "%IMAGE_NAME%:%TAG%" "%BUILD_CONTEXT%"

if %ERRORLEVEL% equ 0 (
    echo.
    echo [OK] Docker image built successfully!
    echo.
    echo [i] Image Information:
    docker images "%IMAGE_NAME%:%TAG%"
    echo.
    echo [*] To start the container, run:
    echo    docker-start.bat
    echo.
    echo    Or manually:
    echo    docker run -d -p 9090:9090 -v "\\.\pipe\docker_engine:\\.\pipe\docker_engine" %IMAGE_NAME%:%TAG%
) else (
    echo.
    echo [X] Docker build failed!
    pause
    exit /b 1
)

echo.
echo Press any key to continue...
pause >nul
