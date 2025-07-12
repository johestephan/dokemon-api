# Dokemon API

<div align="center">

<img src="https://img.shields.io/badge/Dokemon-API-blue?style=for-the-badge" alt="Dokemon API"/>
<img src="https://img.shields.io/badge/Version-1.1.20250712-green?style=for-the-badge" alt="Version"/>
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
    "login_time": "2024-01-15T10:30:00.000000",
    "authenticated": true
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

#### Authentication Security Features

- **Password Hashing**: PBKDF2 with SHA-256 and random salt (100,000 iterations)
- **Session Management**: Flask sessions with configurable timeout (default: 2 hours)
- **File-based Storage**: User data stored in `users.json` (upgrade to database for production)
- **Session Timeout**: Automatic logout after 24 hours of inactivity
- **Password Requirements**: Minimum 8 characters, usernames minimum 3 characters

#### Using Authentication in Requests

After login, include the session cookie in all subsequent requests:

```bash
# Example: List containers with authentication
curl -X GET http://localhost:9090/api/v1/containers \
  -H "Cookie: session=<your_session_cookie>"
```

#### Authentication Curl Examples

##### Create New User
```bash
# Create a new user account
curl -X POST http://localhost:9090/api/v1/users \
  -H "Content-Type: application/json" \
  -d '{
    "username": "newuser",
    "password": "securepassword123",
    "email": "user@example.com"
  }'
```

##### Login (Get Session Cookie)
```bash
# Login and save session cookie
curl -X POST http://localhost:9090/api/v1/users/login \
  -H "Content-Type: application/json" \
  -c cookies.txt \
  -d '{
    "username": "admin",
    "password": "admin"
  }'

# Or login and extract cookie manually
curl -X POST http://localhost:9090/api/v1/users/login \
  -H "Content-Type: application/json" \
  -v \
  -d '{
    "username": "admin",
    "password": "admin"
  }' 2>&1 | grep -i "set-cookie"
```

##### Get Current User Info
```bash
# Get current user information (requires login)
curl -X GET http://localhost:9090/api/v1/users/me \
  -b cookies.txt

# Or with manual cookie
curl -X GET http://localhost:9090/api/v1/users/me \
  -H "Cookie: session=your_session_cookie_here"
```

##### Change Password
```bash
# Change user password (requires login)
curl -X POST http://localhost:9090/api/v1/users/changepassword \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "currentPassword": "admin",
    "newPassword": "newSecurePassword123"
  }'
```

##### Logout (JSON Response)
```bash
# Logout via API (clears session)
curl -X POST http://localhost:9090/api/v1/users/logout \
  -b cookies.txt
```

##### Logout (HTML Page)
```bash
# Access logout page in browser or get HTML response
curl -X GET http://localhost:9090/api/v1/users/logout \
  -b cookies.txt

# Open logout page in browser (for Dokémon NG app)
open http://localhost:9090/api/v1/users/logout
# or visit in browser: http://localhost:9090/api/v1/users/logout
```

##### Complete Authentication Workflow Example
```bash
# 1. Create user
curl -X POST http://localhost:9090/api/v1/users \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "password123", "email": "test@example.com"}'

# 2. Login and save session
curl -X POST http://localhost:9090/api/v1/users/login \
  -H "Content-Type: application/json" \
  -c cookies.txt \
  -d '{"username": "testuser", "password": "password123"}'

# 3. Access protected resources
curl -X GET http://localhost:9090/api/v1/users/me -b cookies.txt
curl -X GET http://localhost:9090/api/v1/containers -b cookies.txt

# 4. Change password
curl -X POST http://localhost:9090/api/v1/users/changepassword \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{"currentPassword": "password123", "newPassword": "newpassword456"}'

# 5. Logout
curl -X POST http://localhost:9090/api/v1/users/logout -b cookies.txt
```
### Container Management

#### List Containers
```bash
GET /api/v1/containers?all=true
```
Returns structured JSON with container details:
```json
{
  "containers": [
    {
      "container_id": "c416bf187ea6",
      "image": "nginx:latest",
      "command": "\"/docker-entrypoint.sh nginx\"",
      "created": "2 hours ago",
      "status": "Up 2 hours",
      "ports": "0.0.0.0:8080->80/tcp",
      "names": "my-nginx"
    }
  ]
}
```

#### Container Operations
- `POST /api/v1/containers/{id}/start` - Start container
- `POST /api/v1/containers/{id}/stop` - Stop container  
- `POST /api/v1/containers/{id}/restart` - Restart container
- `DELETE /api/v1/containers/{id}/remove?force=true` - Remove container
- `GET /api/v1/containers/{id}/logs?tail=100` - Get container logs
- `GET /api/v1/containers/{id}/inspect` - Get detailed container info
- `POST /api/v1/containers/{id}/exec` - Execute command in container

#### Run New Container
```bash
POST /api/v1/containers/run
Content-Type: application/json
```
```json
{
  "image": "postgres:13",
  "name": "my-postgres",
  "detached": true,
  "ports": ["5432:5432"],
  "volumes": ["postgres-data:/var/lib/postgresql/data"],
  "environment": ["POSTGRES_PASSWORD=secret", "POSTGRES_DB=myapp"],
  "command": ""
}
```

### Image Management

#### List Images
```bash
GET /api/v1/images
```
Returns structured data:
```json
{
  "images": [
    {
      "repository": "nginx",
      "tag": "latest",
      "image_id": "f8f4ffc8092c",
      "created": "2 weeks ago",
      "size": "109MB"
    }
  ]
}
```

#### Image Operations
- `POST /api/v1/images/pull` - Pull image from registry
- `DELETE /api/v1/images/{id}/remove?force=true` - Remove image
- `POST /api/v1/images/build` - Build image from Dockerfile

### Network Management

#### List Networks
```bash
GET /api/v1/networks
```
Returns structured network data:
```json
{
  "networks": [
    {
      "network_id": "c416bf187ea6",
      "name": "bridge",
      "driver": "bridge",
      "scope": "local"
    }
  ]
}
```

#### Network Operations
- `POST /api/v1/networks/create` - Create network
- `DELETE /api/v1/networks/{name}/remove` - Remove network

### Volume Management

#### List Volumes
```bash
GET /api/v1/volumes
```
Returns structured volume data:
```json
{
  "volumes": [
    {
      "driver": "local",
      "volume_name": "postgres-data"
    }
  ]
}
```

#### Volume Operations
- `POST /api/v1/volumes/create` - Create volume
- `DELETE /api/v1/volumes/{name}/remove` - Remove volume

### System Operations

#### System Information
- `GET /api/v1/system/info` - Detailed Docker system information
- `GET /api/v1/system/summary` - Key system statistics
- `GET /api/v1/system/stats?no-stream=true` - Container resource usage
- `POST /api/v1/system/prune?force=true` - Clean up unused objects

#### System Summary Example
```json
{
  "success": true,
  "summary": {
    "docker_version": "20.10.17",
    "containers": {
      "total": 5,
      "running": 3,
      "paused": 0,
      "stopped": 2
    },
    "images": 12,
    "storage_driver": "overlay2",
    "operating_system": "Ubuntu 20.04.4 LTS",
    "architecture": "x86_64",
    "cpus": 4,
    "total_memory": "7.775GiB"
  }
}
```

## Usage Examples

### Authentication Setup

```bash
# First, login to get session cookie (using default admin account)
curl -X POST http://localhost:9090/api/v1/users/login \
  -H "Content-Type: application/json" \
  -c cookies.txt \
  -d '{
    "username": "admin",
    "password": "admin"
  }'

# Verify login worked
curl -X GET http://localhost:9090/api/v1/users/me -b cookies.txt

# IMPORTANT: Change default password immediately!
curl -X POST http://localhost:9090/api/v1/users/changepassword \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "currentPassword": "admin",
    "newPassword": "your-secure-password"
  }'
```

### Basic Container Operations

```bash
# Check API health (no authentication required)
curl http://localhost:9090/health

# List all containers (may require authentication)
curl "http://localhost:9090/api/v1/containers?all=true" -b cookies.txt

# Run nginx container
curl -X POST http://localhost:9090/api/v1/containers/run \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "image": "nginx:alpine",
    "name": "web-server",
    "detached": true,
    "ports": ["8080:80"]
  }'

# Check container logs
curl "http://localhost:9090/api/v1/containers/web-server/logs?tail=50" -b cookies.txt

# Execute command in container
curl -X POST http://localhost:9090/api/v1/containers/web-server/exec \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{"command": "nginx -v"}'

# Stop and remove container
curl -X POST http://localhost:9090/api/v1/containers/web-server/stop -b cookies.txt
curl -X DELETE "http://localhost:9090/api/v1/containers/web-server/remove?force=true" -b cookies.txt
```

### Advanced Container with Database

```bash
# Create volume for data persistence
curl -X POST http://localhost:9090/api/v1/volumes/create \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{"name": "postgres-data"}'

# Run PostgreSQL with volume and environment
curl -X POST http://localhost:9090/api/v1/containers/run \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "image": "postgres:13-alpine",
    "name": "database",
    "detached": true,
    "ports": ["5432:5432"],
    "volumes": ["postgres-data:/var/lib/postgresql/data"],
    "environment": [
      "POSTGRES_PASSWORD=secretpassword",
      "POSTGRES_DB=myapp",
      "POSTGRES_USER=appuser"
    ]
  }'
```

### Image Management

```bash
# Pull latest Redis image
curl -X POST http://localhost:9090/api/v1/images/pull \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{"image": "redis:alpine"}'

# List all images
curl http://localhost:9090/api/v1/images -b cookies.txt
curl http://localhost:9090/api/v1/images

# Build custom image
curl -X POST http://localhost:9090/api/v1/images/build \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "tag": "my-app:latest",
    "path": "/path/to/dockerfile/directory",
    "dockerfile": "Dockerfile"
  }'
```

### Network Operations

```bash
# Create custom network
curl -X POST http://localhost:9090/api/v1/networks/create \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "name": "my-network",
    "driver": "bridge"
  }'

# List all networks
curl http://localhost:9090/api/v1/networks -b cookies.txt
```

### System Monitoring

```bash
# Get system summary
curl http://localhost:9090/api/v1/system/summary -b cookies.txt

# Get resource statistics
curl "http://localhost:9090/api/v1/system/stats?no-stream=true" -b cookies.txt

# Clean up unused objects (with confirmation)
curl -X POST "http://localhost:9090/api/v1/system/prune?force=true" -b cookies.txt
```

## Configuration

### Environment Variables

The API supports extensive configuration through environment variables:

```bash
# Server Configuration
DOKEMON_HOST=0.0.0.0          # Server bind address
DOKEMON_PORT=9090             # Server port
DOKEMON_DEBUG=true            # Debug mode (true/false)

# Docker Configuration  
DOKEMON_DOCKER_TIMEOUT=30     # Docker command timeout (seconds)
DOKEMON_VERSION_TIMEOUT=5     # Docker version check timeout

# Security
DOKEMON_ALLOWED_HOSTS=*       # Comma-separated allowed hosts

# Logging
DOKEMON_LOG_LEVEL=INFO        # Log level (DEBUG, INFO, WARNING, ERROR)

# Environment Mode
FLASK_ENV=development         # development, production, default
```

### Configuration Classes

The API uses a sophisticated configuration system:
- **Config**: Base configuration class
- **DevelopmentConfig**: Debug enabled, verbose logging
- **ProductionConfig**: Debug disabled, optimized for production

## Security Considerations

- **Docker Socket Access**: API requires access to Docker socket - use in trusted environments
- **Authentication**: Implemented - Session-based authentication with PBKDF2 password hashing
- **Default Credentials**: Change default admin password (admin/admin) immediately
- **User Data Storage**: Currently file-based (`users.json`) - upgrade to database for production
- **Session Security**: Configure `SECRET_KEY` environment variable for production
- **Network Exposure**: Default binding to 0.0.0.0 - restrict in production
- **Command Execution**: API can execute arbitrary commands in containers
- **Resource Limits**: No built-in resource limiting - monitor usage

## Response Format

### Success Response
```json
{
  "success": true,
  "output": "operation_result_or_data"
}
```

### Error Response
```json
{
  "success": false,
  "error": "Detailed error message"
}
```

### Structured Data Response
```json
{
  "containers": [...],
  "images": [...],
  "networks": [...],
  "volumes": [...]
}
```

## Troubleshooting

### Common Issues

**"Docker is not accessible"**
```bash
# Check Docker status
docker --version
docker info

# On Linux/macOS, check socket
ls -la /var/run/docker.sock

# Restart Docker service if needed
sudo systemctl restart docker  # Linux
# or restart Docker Desktop
```

**"ModuleNotFoundError: No module named 'flask'"**
```bash
# Activate virtual environment
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate.bat  # Windows

# Install requirements
pip install -r requirements.txt
```

**"Permission denied" on Docker socket**
```bash
# Linux - Add user to docker group
sudo usermod -aG docker $USER
# Then logout and login again

# Windows - IMPORTANT: Container must run as root
docker stop dokemon-api && docker rm dokemon-api
docker run -d --name dokemon-api -p 9090:9090 -u root -v "/var/run/docker.sock:/var/run/docker.sock" -v dokemon_data:/app/data javastraat/dokemon-api:latest

# OR use provided Windows scripts which handle this automatically
docker-start.bat  # or .\docker-start.ps1
```

**Windows Docker Desktop Issues**
```cmd
REM "Failed to connect to Docker daemon" or "protocol not available"
REM 1. Check Docker Desktop is running in Linux container mode
REM 2. Use debug endpoint for detailed diagnostics
curl http://localhost:9090/docker-debug

REM 3. Ensure container runs as root (Windows requirement)
docker run -d --name dokemon-api -p 9090:9090 -u root -v "/var/run/docker.sock:/var/run/docker.sock" javastraat/dokemon-api:latest

REM 4. Alternative: Enable Docker TCP API (less secure, development only)
REM Docker Desktop > Settings > General > "Expose daemon on tcp://localhost:2375 without TLS"
docker run -d --name dokemon-api -p 9090:9090 -e DOCKER_HOST=tcp://host.docker.internal:2375 javastraat/dokemon-api:latest
```

> **For comprehensive Windows troubleshooting**, see: [`WINDOWS_DOCKER_TROUBLESHOOTING.md`](WINDOWS_DOCKER_TROUBLESHOOTING.md)

**Port already in use**
```bash
# Change port via environment variable
export DOKEMON_PORT=8080
python app.py

# Or find and kill process using port 9090
lsof -ti:9090 | xargs kill  # macOS/Linux
netstat -ano | findstr :9090  # Windows
```

**Import errors in modular structure**
```bash
# Make sure you're running from the project root
cd /path/to/dokemon-api
python app.py

# Check Python path if needed
export PYTHONPATH=$PYTHONPATH:.
```

## Development

### Adding New Endpoints

**1. To existing module (e.g., add container feature):**
```python
# Edit routes/containers.py
@containers_bp.route('/<container_id>/pause', methods=['POST'])
def pause_container(container_id):
    command = f"docker pause {container_id}"
    response, status = run_docker_command(command)
    return jsonify(response), status
```

**2. New module (e.g., Docker Compose support):**
```python
# Create routes/compose.py
from flask import Blueprint
from utils.docker_utils import run_docker_command

compose_bp = Blueprint('compose', __name__, url_prefix='/api/v1/compose')

@compose_bp.route('/up', methods=['POST'])
def compose_up():
    # Implementation here
    pass
```

```python
# Add to app.py
from routes.compose import compose_bp
app.register_blueprint(compose_bp)
```

### Adding New Utilities

**1. New parser function:**
```python
# Add to utils/parsers.py
def parse_compose_output(output):
    # Implementation here
    pass
```

**2. New utility module:**
```python
# Create utils/new_feature.py
def new_utility_function():
    # Implementation here
    pass
```

### Running in Production

The Dokemon API is now configured to use **Gunicorn** as the production WSGI server for better performance, reliability, and scalability.

#### Quick Start (Production)

```bash
# Using the production startup script
./start-prod.sh

# Or manually
export FLASK_ENV=production
export DOKEMON_DEBUG=false
gunicorn --config gunicorn.conf.py app:app
```

#### Development Mode

For development, you can still use Flask's built-in server:

```bash
# Using the development startup script
./start-dev.sh

# Or manually
export FLASK_ENV=development
export DOKEMON_DEBUG=true
python app.py
```

#### Gunicorn Configuration

The API includes a comprehensive Gunicorn configuration file (`gunicorn.conf.py`) with:

- **Auto-scaling workers**: Automatically determines optimal worker count based on CPU cores
- **Performance tuning**: Request timeouts, connection limits, and worker recycling
- **Logging**: Structured access and error logging to stdout/stderr
- **Security**: Request size limits and other security settings

#### Environment Variables

Control Gunicorn behavior with these environment variables:

```bash
# Server binding
export DOKEMON_HOST=0.0.0.0          # Default: 0.0.0.0
export DOKEMON_PORT=9090              # Default: 9090

# Worker configuration
export GUNICORN_WORKERS=4             # Default: auto (CPU cores * 2 + 1)
export GUNICORN_LOG_LEVEL=info        # Default: info

# Application environment
export FLASK_ENV=production           # Default: production
export DOKEMON_DEBUG=false           # Default: false
```

#### Production Deployment Options

**Option 1: Systemd Service (Recommended)**

```bash
# Copy service file
sudo cp dokemon-api.service /etc/systemd/system/

# Create user and setup application
sudo useradd -r -s /bin/false -G docker dokemon
sudo mkdir -p /opt/dokemon-api
sudo cp -r . /opt/dokemon-api/
sudo chown -R dokemon:dokemon /opt/dokemon-api

# Install dependencies
cd /opt/dokemon-api
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Enable and start service
sudo systemctl enable dokemon-api
sudo systemctl start dokemon-api
sudo systemctl status dokemon-api
```

**Option 2: Docker Deployment**

The Docker image now uses Gunicorn by default:

```bash
# Build and run with Docker Compose
docker-compose up -d

# Or build manually
docker build -t dokemon-api .
docker run -d -p 9090:9090 \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -e FLASK_ENV=production \
  -e DOKEMON_DEBUG=false \
  dokemon-api
```

**Option 3: Manual Deployment**

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export FLASK_ENV=production
export DOKEMON_DEBUG=false

# Start with Gunicorn
gunicorn --config gunicorn.conf.py app:app
```

#### Performance Benefits

Using Gunicorn provides several advantages over Flask's development server:

- **Multiple worker processes**: Better CPU utilization and request handling
- **Process recycling**: Automatic worker restarts prevent memory leaks
- **Production-grade logging**: Structured access logs and error handling
- **Graceful shutdowns**: Proper signal handling for deployments
- **Resource limits**: Built-in protection against resource exhaustion

### Testing

```bash
# Test individual modules
python -m pytest routes/test_containers.py
python -m pytest utils/test_parsers.py

# Test entire API
python -m pytest tests/
```

## Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/new-endpoint`
3. Follow the modular structure
4. Add tests for new functionality
5. Update documentation
6. Submit pull request

### Code Organization Guidelines

- **Routes**: Put endpoint logic in appropriate route module
- **Utils**: Put shared functionality in utils modules
- **Config**: Add new configuration options to `config.py`
- **Documentation**: Update README for new features

## License

This project is part of the Dokemon ecosystem. See project license for details.

## Version History

### **v1.1.20250712** *(Production-Ready WSGI Server)*
**Enhanced production deployment with Gunicorn WSGI server:**

- **Gunicorn Integration**: Production-ready WSGI server replacing Flask development server
- **Auto-scaling Configuration**: Intelligent worker process management based on CPU cores
- **Comprehensive Configuration**: Dedicated `gunicorn.conf.py` with performance tuning
- **Startup Scripts**: Dedicated `start-prod.sh` and `start-dev.sh` for different environments
- **Systemd Service**: Ready-to-use systemd service file for Linux deployments
- **Updated Docker**: Container now uses Gunicorn by default for production deployments
- **Performance Improvements**: Better request handling, worker recycling, and resource management
- **Enhanced Logging**: Structured access logs and error handling for production monitoring
- **Graceful Shutdowns**: Proper signal handling for zero-downtime deployments
- **Documentation Updates**: Comprehensive production deployment guide with multiple options

*This release transforms the API into a production-ready service with enterprise-grade WSGI server capabilities, significantly improving performance, reliability, and deployment flexibility.*

### **v1.0.20250712** *(Initial Release - NOT Production Ready yet)*
**Complete Docker Management API with comprehensive feature set:**

- **Complete Docker Management API**: Full container, image, network, and volume operations
- **Modular Architecture**: Professional Flask Blueprints structure with utils/ and routes/
- **Authentication System**: PBKDF2 password hashing, session management, user creation
- **Cross-Platform Support**: Windows, macOS, and Linux with platform-specific scripts
- **Docker Deployment**: Multi-stage optimized builds (~142MB vs 1.5GB+)
- **Comprehensive Documentation**: Professional README with OpenAPI specification
- **Windows Docker Desktop Support**: Root user execution and socket troubleshooting
- **Environment Configuration**: Flexible config classes and environment variables
- **Professional Error Handling**: Comprehensive timeout management and structured responses
- **Development Tools**: Cross-platform build scripts and setup automation

*This initial release represents a NONE complete, production-ready Docker management API with enterprise-grade features, comprehensive documentation, and cross-platform compatibility.*

