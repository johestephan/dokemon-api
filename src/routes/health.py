#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Blueprint, jsonify
from utils.docker_utils import run_docker_command

# Create blueprint for health and system checks
health_bp = Blueprint('health', __name__)

@health_bp.route('/health', methods=['GET'])
def health_check():
    """Check if Docker is running and accessible"""
    import os
    
    # Read version from version.txt
    try:
        version_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'version.txt')
        with open(version_file_path, 'r') as f:
            software_version = f.read().strip()
    except (FileNotFoundError, IOError):
        software_version = "missing version.txt warning"
    
    response, status = run_docker_command("docker --version")
    if status == 200:
        return jsonify({
            "status": "healthy", 
            "docker_version": response["output"],
            "software_name": "Dokémon NG",
            "software_version": software_version
        })
    else:
        return jsonify({
            "status": "unhealthy", 
            "error": response.get("error"),
            "software_name": "Dokémon NG",
            "software_version": software_version
        }), 500

@health_bp.route('/', methods=['GET'])
def api_documentation():
    """API documentation"""
    from flask import current_app
    import os
    
    # Read version from version.txt
    try:
        version_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'version.txt')
        with open(version_file_path, 'r') as f:
            software_version = f.read().strip()
    except (FileNotFoundError, IOError):
        software_version = "missing version.txt warning"
    
    endpoints = {
        "health": "GET /health - Check Docker status",
        "containers": {
            "list": "GET /api/v1/containers?all=true - List containers",
            "start": "POST /api/v1/containers/{id}/start - Start container",
            "stop": "POST /api/v1/containers/{id}/stop - Stop container", 
            "restart": "POST /api/v1/containers/{id}/restart - Restart container",
            "remove": "DELETE /api/v1/containers/{id}/remove?force=true - Remove container",
            "logs": "GET /api/v1/containers/{id}/logs?tail=100 - Get container logs",
            "inspect": "GET /api/v1/containers/{id}/inspect - Inspect container",
            "exec": "POST /api/v1/containers/{id}/exec - Execute command in container",
            "run": "POST /api/v1/containers/run - Run new container"
        },
        "images": {
            "list": "GET /api/v1/images - List images",
            "pull": "POST /api/v1/images/pull - Pull image",
            "remove": "DELETE /api/v1/images/{id}/remove?force=true - Remove image",
            "build": "POST /api/v1/images/build - Build image"
        },
        "networks": {
            "list": "GET /api/v1/networks - List networks",
            "create": "POST /api/v1/networks/create - Create network",
            "remove": "DELETE /api/v1/networks/{name}/remove - Remove network"
        },
        "volumes": {
            "list": "GET /api/v1/volumes - List volumes",
            "create": "POST /api/v1/volumes/create - Create volume",
            "remove": "DELETE /api/v1/volumes/{name}/remove - Remove volume"
        },
        "system": {
            "info": "GET /api/v1/system/info - System information (detailed)",
            "summary": "GET /api/v1/system/summary - System summary (key stats)",
            "stats": "GET /api/v1/system/stats - Resource statistics",
            "prune": "POST /api/v1/system/prune?force=true - Clean up unused objects"
        },
        "users": {
            "create": "POST /api/v1/users - Create new user",
            "login": "POST /api/v1/users/login - User login",
            "logout_api": "POST /api/v1/users/logout - Logout (JSON response)",
            "logout_page": "GET /api/v1/users/logout - Logout (HTML page)",
            "me": "GET /api/v1/users/me - Current user info",
            "change_password": "POST /api/v1/users/changepassword - Change password",
            "admin_list": "GET /api/v1/users/list - List all users (admin)",
            "admin_info": "GET /api/v1/users/<username>/info - Get user info (admin)",
            "admin_activate": "POST /api/v1/users/<username>/activate - Activate user (admin)",
            "admin_deactivate": "POST /api/v1/users/<username>/deactivate - Deactivate user (admin)",
            "admin_reset": "POST /api/v1/users/<username>/reset-password - Reset password (admin)",
            "admin_promote": "POST /api/v1/users/admin/promote/<username> - Promote to admin",
            "admin_demote": "POST /api/v1/users/admin/demote/<username> - Demote from admin",
            "admin_delete": "DELETE /api/v1/users/<username>/delete - Delete user (admin)"
        }
    }
    
    return jsonify({
        "message": current_app.config.get('API_NAME', 'Dokémon NG API'),
        "version": software_version,
        "description": current_app.config.get('API_DESCRIPTION', 'A RESTful API for Docker management'),
        "software_name": "Dokémon NG",
        "endpoints": endpoints
    })

@health_bp.route('/docker-debug', methods=['GET'])
def docker_debug():
    """Detailed Docker connectivity diagnostics"""
    import os
    import subprocess
    from flask import current_app
    
    debug_info = {
        "platform": os.name,
        "tests": {}
    }
    
    # Test 1: Docker CLI availability
    try:
        result = subprocess.run(['docker', '--version'], capture_output=True, text=True, timeout=5)
        debug_info["tests"]["docker_cli"] = {
            "status": "success" if result.returncode == 0 else "failed",
            "output": result.stdout.strip(),
            "error": result.stderr.strip() if result.stderr else None
        }
    except Exception as e:
        debug_info["tests"]["docker_cli"] = {
            "status": "failed",
            "error": str(e)
        }
    
    # Test 2: Docker daemon connectivity
    try:
        result = subprocess.run(['docker', 'info'], capture_output=True, text=True, timeout=10)
        debug_info["tests"]["docker_daemon"] = {
            "status": "success" if result.returncode == 0 else "failed",
            "output": result.stdout.strip() if result.returncode == 0 else None,
            "error": result.stderr.strip() if result.stderr else None
        }
    except Exception as e:
        debug_info["tests"]["docker_daemon"] = {
            "status": "failed",
            "error": str(e)
        }
    
    # Test 3: Socket file checks
    socket_paths = [
        '/var/run/docker.sock',
        '/var/run/docker.sock.raw',
        '~/.docker/run/docker.sock',
        '~/.docker/desktop/docker.sock'
    ]
    
    debug_info["tests"]["socket_files"] = {}
    for path in socket_paths:
        expanded_path = os.path.expanduser(path)
        debug_info["tests"]["socket_files"][path] = {
            "exists": os.path.exists(expanded_path),
            "expanded_path": expanded_path
        }
        if os.path.exists(expanded_path):
            try:
                stat = os.stat(expanded_path)
                debug_info["tests"]["socket_files"][path]["permissions"] = oct(stat.st_mode)
            except Exception as e:
                debug_info["tests"]["socket_files"][path]["error"] = str(e)
    
    # Test 4: Environment variables
    debug_info["environment"] = {
        "DOCKER_HOST": os.environ.get("DOCKER_HOST"),
        "DOCKER_TLS_VERIFY": os.environ.get("DOCKER_TLS_VERIFY"),
        "DOCKER_CERT_PATH": os.environ.get("DOCKER_CERT_PATH")
    }
    
    # Test 5: Simple container list
    try:
        result = subprocess.run(['docker', 'ps', '--format', 'json'], capture_output=True, text=True, timeout=10)
        debug_info["tests"]["container_list"] = {
            "status": "success" if result.returncode == 0 else "failed",
            "output": result.stdout.strip() if result.returncode == 0 else None,
            "error": result.stderr.strip() if result.stderr else None
        }
    except Exception as e:
        debug_info["tests"]["container_list"] = {
            "status": "failed",
            "error": str(e)
        }
    
    return jsonify({
        "debug_info": debug_info,
        "recommendation": get_docker_recommendation(debug_info)
    })

def get_docker_recommendation(debug_info):
    """Provide troubleshooting recommendations based on debug info"""
    recommendations = []
    
    if debug_info["tests"]["docker_cli"]["status"] == "failed":
        recommendations.append("Docker CLI is not available. Install Docker or check PATH.")
    
    if debug_info["tests"]["docker_daemon"]["status"] == "failed":
        error_msg = str(debug_info["tests"]["docker_daemon"].get("error", "")).lower()
        if "permission denied" in error_msg:
            recommendations.append("SOLUTION: Docker socket permission denied. Restart container with: docker run -u root")
            recommendations.append("Run: docker stop dokemon-api && docker rm dokemon-api")
            recommendations.append("Then: docker run -d --name dokemon-api -p 9090:9090 -u root -v \"/var/run/docker.sock:/var/run/docker.sock\" -v dokemon_data:/app/data javastraat/dokemon-api:latest")
        elif "protocol not available" in error_msg:
            recommendations.append("SOLUTION: Windows Docker socket protocol issue. Try running with root user and standard socket mount.")
        else:
            recommendations.append("Cannot connect to Docker daemon. Ensure Docker is running.")
    
    if debug_info["platform"] == "nt":  # Windows
        recommendations.append("Windows detected. Ensure Docker Desktop is running and using Linux containers.")
        recommendations.append("For Windows, use socket mount: -v \"/var/run/docker.sock:/var/run/docker.sock\"")
        recommendations.append("Important: Run container as root user with -u root flag")
    
    if not any(info["exists"] for info in debug_info["tests"]["socket_files"].values()):
        recommendations.append("No Docker socket files found. Check Docker installation.")
    
    # Check if we're running as non-root user
    import os
    current_user = os.getuid() if hasattr(os, 'getuid') else "unknown"
    if current_user != 0 and debug_info["tests"]["docker_daemon"]["status"] == "failed":
        recommendations.append(f"Running as user ID {current_user} (not root). Docker socket usually requires root access.")
        recommendations.append("SOLUTION: Restart container with -u root flag")
    
    if not recommendations:
        recommendations.append("All tests passed. Docker should be working properly.")
    
    return recommendations
