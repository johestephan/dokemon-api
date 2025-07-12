# Dokemon API

<div align="center">

<img src="https://img.shields.io/badge/Dokemon-API-blue?style=for-the-badge" alt="Dokemon API"/>
<img src="https://img.shields.io/badge/Version-1.0.20250712-green?style=for-the-badge" alt="Version"/>
<img src="https://img.shields.io/badge/Docker-Management-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker"/>
<img src="https://img.shields.io/badge/Flask-API-000000?style=for-the-badge&logo=flask&logoColor=white" alt="Flask"/>
<img src="https://img.shields.io/badge/Gunicorn-WSGI-4B8BBE?style=for-the-badge&logo=gunicorn&logoColor=white" alt="Gunicorn"/>

<h2 align="center">A comprehensive RESTful API server for Docker management</h2>

<p align="center"><em>Part of the Dokemon project ecosystem</em></p>

<p align="center">
<a href="#quick-start">Quick Start</a> • 
<a href="#api-documentation">Documentation</a> • 
<a href="#docker-deployment">Docker Deployment</a> • 
<a href="#development-guide">Development</a>
</p>

</div>

---

## Table of Contents

### **Overview**
- [Features](#features)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)

### **Getting Started**
- [Quick Start](#quick-start)
- [Installation](#installation)
  - [Windows Installation](#windows-installation)
  - [macOS/Linux Installation](#macoslinux-installation)
- [Server Configuration](#server-configuration)

### **Docker Deployment**
- [Docker Overview](#docker-overview)
- [Quick Start with Docker Compose](#quick-start-with-docker-compose)
- [Manual Docker Build](#manual-docker-build)
- [Docker Configuration](#docker-configuration)
- [Production Deployment](#production-deployment)
- [Docker Troubleshooting](#docker-troubleshooting)

### **API Documentation**
- [Authentication System](#user-authentication)
- [Container Management](#container-management)
- [Image Management](#image-management)
- [Network Management](#network-management)
- [Volume Management](#volume-management)
- [System Operations](#system-operations)
- [Usage Examples](#usage-examples)

### **Configuration & Security**
- [Environment Variables](#environment-variables)
- [Security Considerations](#security-considerations)
- [Response Formats](#response-formats)

### **Development & Support**
- [Troubleshooting](#troubleshooting)
- [Development Guide](#development-guide)
- [Contributing](#contributing)
- [License](#license)
- [Version History](#version-history)

---

## Features

### **Docker Management**
- **Complete Container Management**: Start, stop, restart, remove, run new containers with advanced options
- **Image Management**: List, pull, remove, build images with detailed information
- **Network Management**: Create, list, remove networks with structured data
- **Volume Management**: Create, list, remove volumes with proper formatting
- **System Operations**: Get detailed info, stats, and cleanup operations
- **Logging & Monitoring**: View container logs and real-time resource usage

### **Security & Authentication**
- **User Authentication & Session Management**: Secure API access with login/logout
- **Password Management**: PBKDF2 hashing with secure password change functionality
- **Session-based Security**: Configurable session timeouts and secure cookies
- **Default Admin Setup**: Ready-to-use admin account with forced password change

### **Architecture & Performance**
- **Modular Architecture**: Clean, maintainable code structure using Flask Blueprints
- **Structured JSON Responses**: All endpoints return clean, parsed JSON data
- **Professional Error Handling**: Comprehensive error responses and timeout management
- **Environment-Based Configuration**: Flexible config management with environment variables
- **Optimized Docker Image**: Multi-stage build produces ~142MB image (10x smaller than standard Docker installs)

### **Platform Support**
- **Cross-Platform Support**: Works on Windows, macOS, and Linux
- **Docker Desktop Compatibility**: Special handling for Windows Docker Desktop socket access
- **Containerized Deployment**: Ready-to-use Docker containers with Docker Compose support
- **Development Tools**: Comprehensive build scripts for all platforms

---

## Quick Start

### **Fastest Setup (Docker)**
```bash
# Clone repository
git clone <repository-url>
cd dokemon-api

# Start with Docker Compose (recommended)
docker-compose up -d

# Access the API
curl http://localhost:9090/health
```

### **Native Installation**

**Windows:**
```cmd
setup_windows.bat && start_windows.bat
```

**macOS/Linux:**
```bash
chmod +x setup.sh && ./setup.sh && python app.py
```

### **First Access**
1. **API Health**: http://localhost:9090/health
2. **Documentation**: http://localhost:9090/
3. **Default Login**: `admin` / `admin` (Change immediately!)

---

## Project Structure

The Dokemon API uses a professional modular architecture for easy maintenance and scalability:

```
dokemon-api/
├── app.py                         # Main application (45 lines - clean & simple!)
├── config.py                      # Configuration management
├── requirements.txt               # Python dependencies
├── README.md                     # This documentation
├── version.txt                   # Software version
├── setup.sh                      # Linux/macOS setup script
├── setup_windows.bat             # Windows setup script
├── setup_windows.ps1             # PowerShell setup script
├── start_windows.bat             # Windows start script
├── WINDOWS_SETUP.md              # Windows-specific guide
├── WINDOWS_DOCKER_TROUBLESHOOTING.md  # Windows Docker troubleshooting
├── Dockerfile                    # Optimized Docker container (multi-stage build)
├── docker-compose.yml            # Docker Compose configuration
├── docker-build.sh               # Linux/macOS Docker build script
├── docker-start.sh               # Linux/macOS Docker start script  
├── docker-build.bat              # Windows Docker build script
├── docker-start.bat              # Windows Docker start script
├── docker-build.ps1              # PowerShell Docker build script
├── docker-start.ps1              # PowerShell Docker start script
├── nginx.conf                    # Nginx reverse proxy config
├── .dockerignore                 # Docker build exclusions
├── dokemon-api.yaml              # OpenAPI specification for RapidAPI
├── utils/                        # Utility modules
│   ├── __init__.py
│   ├── auth.py                   # Authentication & user management
│   ├── docker_utils.py           # Docker command execution
│   └── parsers.py                # Data parsing functions
└── routes/                       # Modular route blueprints
    ├── __init__.py
    ├── health.py                 # Health check & API documentation
    ├── containers.py             # Container management endpoints
    ├── images.py                 # Image management endpoints
    ├── networks.py               # Network management endpoints
    ├── volumes.py                # Volume management endpoints
    ├── users.py                  # User authentication endpoints
    └── system.py                 # System operations endpoints
```

### **Modular Benefits:**

- **Organized by Functionality**: Each module handles one specific area
- **Easy Maintenance**: Add new features by editing relevant module
- **Testable**: Each module can be tested independently
- **Readable**: Clear separation of concerns
- **Scalable**: Easy to extend with new endpoints or features

### **Module Breakdown:**

| Module | Purpose | Endpoints |
|--------|---------|-----------|
| `health.py` | Health checks & API docs | `/health`, `/` |
| `containers.py` | Container operations | `/api/v1/containers/*` |
| `images.py` | Image operations | `/api/v1/images/*` |
| `networks.py` | Network operations | `/api/v1/networks/*` |
| `volumes.py` | Volume operations | `/api/v1/volumes/*` |
| `system.py` | System operations | `/api/v1/system/*` |
| `users.py` | User authentication | `/api/v1/users/*` |
| `auth.py` | Authentication utilities | Shared utility |
| `docker_utils.py` | Docker command execution | Shared utility |
| `parsers.py` | Output parsing | Shared utility |

## Prerequisites

- Python 3.6+ 
- Docker installed and running
- Access to Docker socket (`/var/run/docker.sock` on Unix, named pipe on Windows)

## Installation

### Windows Installation

#### **Option 1: Automated Setup (Recommended)**
```cmd
# Quick setup - Run both scripts
setup_windows.bat
start_windows.bat
```

#### **Option 2: PowerShell**
```powershell
# PowerShell setup
.\setup_windows.ps1

# Activate environment and start
venv\Scripts\Activate.ps1
python app.py
```

#### **Option 3: Manual Setup**
```cmd
# Manual installation
python -m venv venv
venv\Scripts\activate.bat
pip install Flask==2.0.3
python app.py
```

### macOS/Linux Installation

#### **Automated Setup**
```bash
# Make executable and run setup
chmod +x setup.sh
./setup.sh

# Start server
source venv/bin/activate
python app.py
```

#### **Manual Setup**
```bash
# Manual installation
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

---

## Docker Deployment

### Optimized Docker Image

The Dokemon API uses a **multi-stage Docker build** for minimal image size:
- **Final image size**: ~142MB (vs 1.5GB+ with standard Docker installation)
- **Base image**: Python 3.11-slim 
- **Docker CLI**: Only the CLI binary is included (not the full Docker suite)
- **Health checks**: Uses Python built-ins instead of external tools

### Quick Start with Docker Compose

**Prerequisites:**
- Docker and Docker Compose installed
- Docker daemon running

**Simple Deployment:**
```bash
# Clone and navigate to project
git clone <repository-url>
cd dokemon-api

# Start with Docker Compose
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f dokemon-api

# Stop services
docker-compose down
```

**Production Deployment with Nginx:**
```bash
# Start with production profile (includes Nginx reverse proxy)
docker-compose --profile production up -d

# Access via Nginx proxy
curl http://localhost/health
```

### Docker Build Scripts (Automated)

**Linux/macOS:**
```bash
# Build the Docker image
./docker-build.sh

# Start the container
./docker-start.sh

# Or with custom options
./docker-build.sh dokemon-ng/dokemon-api custom-tag
./docker-start.sh dokemon-ng/dokemon-api custom-tag dokemon-container 8080 9090
```

**Windows (Batch Scripts):**
```cmd
REM Build the Docker image
docker-build.bat

REM Start the container
docker-start.bat

REM Or with custom options
docker-build.bat javastraat/dokemon-api custom-tag
docker-start.bat javastraat/dokemon-api custom-tag dokemon-container 8080 9090
```

**Windows (PowerShell):**
```powershell
# Build the Docker image
.\docker-build.ps1

# Start the container
.\docker-start.ps1

# Or with custom parameters
.\docker-build.ps1 -ImageName "javastraat/dokemon-api" -Tag "custom-tag"
.\docker-start.ps1 -ImageName "javastraat/dokemon-api" -Tag "custom-tag" -ContainerName "dokemon-container" -HostPort 8080
```

> **Windows Docker Socket Solution:**  
> **IMPORTANT**: For Windows Docker Desktop compatibility, the container must run as **root user** to access the Docker socket properly. The Windows scripts automatically use `-u root` flag and mount `/var/run/docker.sock:/var/run/docker.sock`. This matches the configuration of working Docker management containers. If you get "permission denied" errors, ensure:
> - Docker Desktop is running in **Linux container mode** (not Windows containers)
> - Use the provided scripts which include the `-u root` flag
> - For troubleshooting, visit: `http://localhost:9090/docker-debug`

### Manual Docker Build Options

**Build Docker Image:**
```bash
# Build the image
docker build -t javastraat/dokemon-api:latest .

# Run container (Linux/macOS)
docker run -d \
  --name dokemon-api \
  -p 9090:9090 \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v dokemon_data:/app/data \
  -e SECRET_KEY=your-secure-secret-key \
  javastraat/dokemon-api:latest

# Run container (Windows)
docker run -d ^
  --name dokemon-api ^
  -p 9090:9090 ^
  -u root ^
  -v "/var/run/docker.sock:/var/run/docker.sock" ^
  -v dokemon_data:/app/data ^
  -e SECRET_KEY=your-secure-secret-key ^
  javastraat/dokemon-api:latest
```

**Windows Important Note:**
The Windows container **must run as root** (`-u root`) to access Docker socket properly. This is required for Docker Desktop compatibility and matches the configuration of other working Docker management tools.

**With Custom Environment:**
```bash
# Create environment file
cat > .env << EOF
SECRET_KEY=your-super-secure-secret-key-here
DEFAULT_ADMIN_PASSWORD=your-admin-password
DOKEMON_DEBUG=false
FLASK_ENV=production
EOF

# Run with environment file
docker-compose --env-file .env up -d
```

### Docker Configuration

**Environment Variables for Container:**
```bash
# Core settings
FLASK_ENV=production              # Application environment
DOKEMON_HOST=0.0.0.0             # Bind host
DOKEMON_PORT=9090                # Application port
DOKEMON_DEBUG=false              # Debug mode

# Security
SECRET_KEY=change-in-production   # Flask secret key
DEFAULT_ADMIN_PASSWORD=admin      # Default admin password

# Docker settings
DOKEMON_DOCKER_TIMEOUT=60        # Docker command timeout
DOKEMON_VERSION_TIMEOUT=10       # Version check timeout
```

**Volume Mounts:**
```bash
# Required: Docker socket for container management
-v /var/run/docker.sock:/var/run/docker.sock

# Recommended: Persistent data storage
-v dokemon_data:/app/data

# Optional: Custom configuration
-v ./config:/app/config:ro
```

**Port Mapping:**
```bash
# Default API port
-p 9090:9090

# With Nginx proxy
-p 80:80      # HTTP
-p 443:443    # HTTPS (if SSL configured)
```

### Production Considerations

**Security:**
```bash
# Use Docker secrets for sensitive data
echo "your-secret-key" | docker secret create dokemon_secret_key -

# Run with non-root user (already configured in Dockerfile)
# Docker socket permissions handled automatically
```

**Monitoring:**
```bash
# Health checks are built-in
docker-compose ps          # Check container status
docker-compose logs -f     # Follow logs
curl http://localhost:9090/health  # API health check
```

**Scaling:**
```bash
# Scale API service (if using load balancer)
docker-compose up -d --scale dokemon-api=3

# Note: Docker socket sharing requires careful consideration for scaling
```

**Backup and Restore:**
```bash
# Backup user data
docker run --rm -v dokemon_data:/data -v $(pwd):/backup alpine \
  tar czf /backup/dokemon-backup.tar.gz -C /data .

# Restore user data
docker run --rm -v dokemon_data:/data -v $(pwd):/backup alpine \
  tar xzf /backup/dokemon-backup.tar.gz -C /data
```

### Docker Troubleshooting

**Common Issues:**

**"Permission denied" accessing Docker socket:**
```bash
# Check Docker socket permissions
ls -la /var/run/docker.sock

# Ensure Docker daemon is running
sudo systemctl status docker

# For rootless Docker, adjust socket path
-v ${XDG_RUNTIME_DIR}/docker.sock:/var/run/docker.sock
```

**Container won't start:**
```bash
# Check logs
docker-compose logs dokemon-api

# Check environment variables
docker-compose exec dokemon-api env | grep DOKEMON

# Verify Docker socket mount
docker-compose exec dokemon-api docker --version
```

**Port conflicts:**
```bash
# Change port in docker-compose.yml
ports:
  - "8080:9090"  # Use port 8080 instead

# Or use environment variable
DOKEMON_PORT=8080 docker-compose up -d
```

## Server Configuration

### **Environment Variables**

The API server runs on `http://localhost:9090` by default and supports extensive configuration:

#### **Core Server Settings**
```bash
# Server binding and networking
export DOKEMON_HOST=0.0.0.0      # Server bind address (0.0.0.0 for all interfaces)
export DOKEMON_PORT=9090          # Server port (default: 9090)
export DOKEMON_DEBUG=false        # Debug mode (true/false)

# Application environment
export FLASK_ENV=production       # Environment mode (development/production/default)
```

#### **Docker Integration Settings**
```bash
# Docker command execution
export DOKEMON_DOCKER_TIMEOUT=60    # Docker command timeout (seconds)
export DOKEMON_VERSION_TIMEOUT=10   # Docker version check timeout (seconds)
```

#### **Security & Authentication**
```bash
# Session security (CRITICAL for production)
export SECRET_KEY=your-super-secure-secret-key-change-in-production

# User management
export DEFAULT_ADMIN_PASSWORD=admin  # Default admin password (change immediately!)

# Network security
export DOKEMON_ALLOWED_HOSTS=*       # Comma-separated allowed hosts
```

#### **Logging & Monitoring**
```bash
# Application logging
export DOKEMON_LOG_LEVEL=INFO        # Log level (DEBUG, INFO, WARNING, ERROR)
```

### **Application Startup**

When you run the API, you'll see a comprehensive startup display:

```
Starting Dokemon API on port 9090...
Docker Management API - A RESTful interface for Docker operations
Make sure Docker is running and accessible via /var/run/docker.sock
API Documentation available at: http://localhost:9090/

Modular Structure:
   - Health & Documentation: /health, /
   - Containers: /api/v1/containers/*
   - Images: /api/v1/images/*
   - Networks: /api/v1/networks/*
   - Volumes: /api/v1/volumes/*
   - System: /api/v1/system/*
   - Users: /api/v1/users/*

Authentication:
   - Create User: POST /api/v1/users
   - Login: POST /api/v1/users/login
   - Logout (JSON): POST /api/v1/users/logout
   - Logout (HTML): GET /api/v1/users/logout
   - Change Password: POST /api/v1/users/changepassword
   - Current User: GET /api/v1/users/me
   Default admin user: admin/admin (change password immediately!)
```

### **Configuration Classes**

The API uses a sophisticated configuration system with multiple environments:

| Configuration | Description | Use Case |
|---------------|-------------|----------|
| `DevelopmentConfig` | Debug enabled, verbose logging | Local development |
| `ProductionConfig` | Debug disabled, optimized performance | Production deployment |
| `Config` (Base) | Default settings and shared configuration | Base class |

---

## API Documentation

### Health & System Check
- `GET /health` - Check Docker daemon status and API health
- `GET /` - API documentation and endpoint overview
- `GET /docker-debug` - **Detailed Docker connectivity diagnostics** (troubleshooting)

#### Docker Debug Endpoint
**Essential for troubleshooting Docker connectivity issues, especially on Windows:**

```bash
# Get detailed Docker diagnostics
curl http://localhost:9090/docker-debug

# Example response includes:
# - Docker CLI availability test
# - Docker daemon connectivity test  
# - Socket file existence checks
# - Environment variables analysis
# - Container listing test
# - Platform-specific recommendations
```

**Use this endpoint when you encounter:**
- "Failed to connect to Docker daemon" errors
- "Protocol not available" errors
- "Permission denied" socket errors
- Any Docker connectivity issues

The endpoint provides actionable troubleshooting steps and exact commands to fix issues.

### User Authentication

The Dokemon API includes a comprehensive authentication system with session-based login, secure password hashing (PBKDF2), and user management capabilities.

#### Default Admin Account
When first started, the API creates a default admin user:
- **Username**: `admin`
- **Password**: `admin`
- **Important**: Change this password immediately after first login!

#### Authentication Endpoints

##### Create User
```bash
POST /api/v1/users
Content-Type: application/json

{
  "username": "newuser",
  "password": "securepassword123",
  "email": "user@example.com"
}
```

**Response:**
```json
{
  "success": true,
  "message": "User created successfully",
  "username": "newuser"
}
```

##### Login
```bash
POST /api/v1/users/login
Content-Type: application/json

{
  "username": "admin",
  "password": "admin"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Authentication successful",
  "username": "admin"
}
```

*Note: Sets authentication session cookie for subsequent requests*

##### Get Current User Info
```bash
GET /api/v1/users/me
Cookie: session=<session_cookie>
```

**Response:**
```json
{
  "success": true,
  "user": {
    "username": "admin",
    "email": "admin@dokemon.local",
    "created_at": "2025-07-12T10:30:00.000000",
    "last_login": "2025-07-12T15:45:00.000000",
    "login_time": "2025-07-12T15:45:00.000000",
    "authenticated": true,
    "is_admin": true
  }
}
```

##### Change Password
```bash
POST /api/v1/users/changepassword
Content-Type: application/json
Cookie: session=<session_cookie>

{
  "currentPassword": "admin",
  "newPassword": "newSecurePassword123"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Password changed successfully"
}
```

##### Logout

**API Logout (JSON Response)**
```bash
POST /api/v1/users/logout
Cookie: session=<session_cookie>
```

**Response:**
```json
{
  "success": true,
  "message": "Logged out successfully",
  "username": "admin"
}
```

**Web Logout (HTML Page)**
```bash
GET /api/v1/users/logout
Cookie: session=<session_cookie>
```

**Response:** Returns HTML page with "Dokémon NG" title and logout confirmation message. Perfect for browser-based applications that need a user-friendly logout page.

##### Admin User Management Endpoints

**Note**: All admin endpoints require authentication with an admin user account.

##### List All Users
```bash
GET /api/v1/users/list
Cookie: session=<admin_session_cookie>
```

**Response:**
```json
{
  "success": true,
  "users": [
    {
      "username": "admin",
      "email": "admin@dokemon.local",
      "created_at": "2025-07-12T10:00:00.000000",
      "last_login": "2025-07-12T15:45:00.000000",
      "active": true,
      "is_admin": true
    },
    {
      "username": "testuser",
      "email": "test@example.com",
      "created_at": "2025-07-12T11:00:00.000000",
      "last_login": "2025-07-12T14:30:00.000000",
      "active": true,
      "is_admin": false
    }
  ],
  "count": 2
}
```

##### Get User Details
```bash
GET /api/v1/users/<username>/info
Cookie: session=<admin_session_cookie>
```

**Response:**
```json
{
  "success": true,
  "user": {
    "username": "testuser",
    "email": "test@example.com",
    "created_at": "2025-07-12T11:00:00.000000",
    "last_login": "2025-07-12T14:30:00.000000",
    "active": true,
    "is_admin": false
  }
}
```

##### Deactivate User Account
```bash
POST /api/v1/users/<username>/deactivate
Cookie: session=<admin_session_cookie>
```

**Response:**
```json
{
  "success": true,
  "message": "User account deactivated"
}
```

##### Activate User Account
```bash
POST /api/v1/users/<username>/activate
Cookie: session=<admin_session_cookie>
```

**Response:**
```json
{
  "success": true,
  "message": "User account activated"
}
```

##### Delete User Account
```bash
DELETE /api/v1/users/<username>/delete
Cookie: session=<admin_session_cookie>
```

**Response:**
```json
{
  "success": true,
  "message": "User account deleted"
}
```

##### Reset User Password (Admin)
```bash
POST /api/v1/users/<username>/reset-password
Content-Type: application/json
Cookie: session=<admin_session_cookie>

{
  "newPassword": "newSecurePassword123"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Password reset successfully"
}
```

##### Promote User to Admin
```bash
POST /api/v1/users/admin/promote/<username>
Cookie: session=<admin_session_cookie>
```

**Response:**
```json
{
  "success": true,
  "message": "User promoted to admin"
}
```

##### Demote User from Admin
```bash
POST /api/v1/users/admin/demote/<username>
Cookie: session=<admin_session_cookie>
```

**Response:**
```json
{
  "success": true,
  "message": "User demoted from admin"
}
```

#### Admin Curl Examples

##### List All Users
```bash
# Get list of all users (admin only)
curl -X GET http://localhost:9090/api/v1/users/list \
  -b cookies.txt
```

##### User Account Management
```bash
# Get specific user information
curl -X GET http://localhost:9090/api/v1/users/testuser/info \
  -b cookies.txt

# Deactivate a user account
curl -X POST http://localhost:9090/api/v1/users/testuser/deactivate \
  -b cookies.txt

# Activate a user account
curl -X POST http://localhost:9090/api/v1/users/testuser/activate \
  -b cookies.txt

# Reset user password (admin bypass)
curl -X POST http://localhost:9090/api/v1/users/testuser/reset-password \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{"newPassword": "newResetPassword123"}'

# Promote user to admin
curl -X POST http://localhost:9090/api/v1/users/admin/promote/testuser \
  -b cookies.txt

# Demote user from admin
curl -X POST http://localhost:9090/api/v1/users/admin/demote/testuser \
  -b cookies.txt

# Delete user account (permanent)
curl -X DELETE http://localhost:9090/api/v1/users/testuser/delete \
  -b cookies.txt
```

##### Complete Admin User Management Workflow
```bash
# 1. Login as admin
curl -X POST http://localhost:9090/api/v1/users/login \
  -H "Content-Type: application/json" \
  -c cookies.txt \
  -d '{"username": "admin", "password": "admin"}'

# 2. List all users
curl -X GET http://localhost:9090/api/v1/users/list \
  -b cookies.txt

# 3. Get specific user details
curl -X GET http://localhost:9090/api/v1/users/testuser/info \
  -b cookies.txt

# 4. Manage user account status
curl -X POST http://localhost:9090/api/v1/users/testuser/deactivate \
  -b cookies.txt

curl -X POST http://localhost:9090/api/v1/users/testuser/activate \
  -b cookies.txt

# 5. Admin privilege management
curl -X POST http://localhost:9090/api/v1/users/admin/promote/testuser \
  -b cookies.txt

# 6. Reset user password
curl -X POST http://localhost:9090/api/v1/users/testuser/reset-password \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{"newPassword": "newAdminSetPassword123"}'

# 7. Final cleanup (if needed)
curl -X DELETE http://localhost:9090/api/v1/users/testuser/delete \
  -b cookies.txt
```

