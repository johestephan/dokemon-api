@echo off
REM Dokemon API - Docker Start Script (Windows)
REM This script starts the Dokemon API container

setlocal EnableDelayedExpansion

echo [*] Dokemon API - Docker Start Script
echo ====================================

REM Variables
set IMAGE_NAME=javastraat/dokemon-api
set TAG=latest
set CONTAINER_NAME=dokemon-api
set HOST_PORT=9090
set CONTAINER_PORT=9090

REM Check if Docker is running
docker info >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [X] Error: Docker is not running or not accessible
    echo Please start Docker Desktop and try again.
    pause
    exit /b 1
)

REM Check if image exists locally, if not Docker will pull from Docker Hub
docker image inspect "%IMAGE_NAME%:%TAG%" >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [i] Image '%IMAGE_NAME%:%TAG%' not found locally
    echo [+] Docker will automatically pull from Docker Hub when starting container...
)

REM Stop and remove existing container if it exists
docker ps -a --format "table {{.Names}}" | findstr /R "^%CONTAINER_NAME%$" >nul 2>&1
if %ERRORLEVEL% equ 0 (
    echo [!] Stopping existing container '%CONTAINER_NAME%'...
    docker stop "%CONTAINER_NAME%" >nul 2>&1
    echo [-] Removing existing container '%CONTAINER_NAME%'...
    docker rm "%CONTAINER_NAME%" >nul 2>&1
)

echo [i] Container Information:
echo    Container Name: %CONTAINER_NAME%
echo    Image: %IMAGE_NAME%:%TAG%
echo    Port Mapping: %HOST_PORT%:%CONTAINER_PORT%
echo    Docker Socket: Windows Docker Desktop compatibility mode
echo.

REM Set default environment variables if not set
if "%SECRET_KEY%"=="" set SECRET_KEY=dokemon-change-this-secret-key
if "%DEFAULT_ADMIN_PASSWORD%"=="" set DEFAULT_ADMIN_PASSWORD=admin

REM Start the container with Windows Docker Desktop compatibility
echo [+] Starting Dokemon API container...
docker run -d ^
    --name "%CONTAINER_NAME%" ^
    -p "%HOST_PORT%:%CONTAINER_PORT%" ^
    -u root ^
    -v "/var/run/docker.sock:/var/run/docker.sock" ^
    -v dokemon_data:/app/data ^
    -e SECRET_KEY=%SECRET_KEY% ^
    -e DEFAULT_ADMIN_PASSWORD=%DEFAULT_ADMIN_PASSWORD% ^
    --restart unless-stopped ^
    "%IMAGE_NAME%:%TAG%"

if %ERRORLEVEL% equ 0 (
    echo.
    echo [OK] Container started successfully!
    echo.
    echo [i] Container Status:
    docker ps --filter "name=%CONTAINER_NAME%"
    echo.
    echo [*] API Access:
    echo    Health Check: http://localhost:%HOST_PORT%/health
    echo    Docker Debug: http://localhost:%HOST_PORT%/docker-debug
    echo    API Documentation: http://localhost:%HOST_PORT%/
    echo    Default Login: admin/admin ^(change immediately!^)
    echo.
    echo [i] Useful Commands:
    echo    View logs: docker logs -f %CONTAINER_NAME%
    echo    Stop container: docker stop %CONTAINER_NAME%
    echo    Remove container: docker rm %CONTAINER_NAME%
    echo.
    echo [!] Remember to change the default admin password!
    echo.
    echo [i] If you get Docker permission errors in the API:
    echo    1. Visit http://localhost:%HOST_PORT%/docker-debug for diagnostics
    echo    2. Ensure Docker Desktop is running in Linux container mode
    echo    3. Try restarting Docker Desktop
    echo    4. Check Docker Desktop settings ^> Resources ^> File Sharing
) else (
    echo.
    echo [X] Failed to start container!
    echo.
    echo [i] Troubleshooting steps:
    echo    1. Make sure Docker Desktop is running
    echo    2. Check if the image exists: docker images %IMAGE_NAME%:%TAG%
    echo    3. Try building the image: docker-build.bat
    echo    4. Check for port conflicts: netstat -an ^| findstr :%HOST_PORT%
    echo    5. Try running as Administrator
    pause
    exit /b 1
)

echo.
echo Press any key to continue...
pause >nul
