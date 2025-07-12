#!/usr/bin/env python3

import subprocess
import json
import os
from flask import current_app

def run_docker_command(command):
    """Execute a docker command and return the result"""
    try:
        # First, test Docker connectivity
        try:
            version_timeout = current_app.config.get('DOCKER_VERSION_TIMEOUT', 10)
            version_result = subprocess.run(['docker', '--version'], capture_output=True, check=True, timeout=version_timeout, text=True)
            current_app.logger.info(f"Docker version check passed: {version_result.stdout.strip()}")
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired) as e:
            current_app.logger.error(f"Docker version check failed: {e}")
            return {"error": "Docker is not accessible. Is Docker running?", "success": False}, 500
        
        # Test Docker daemon connectivity
        try:
            daemon_timeout = current_app.config.get('DOCKER_VERSION_TIMEOUT', 10)
            daemon_result = subprocess.run(['docker', 'info'], capture_output=True, check=True, timeout=daemon_timeout, text=True)
            current_app.logger.info("Docker daemon connectivity verified")
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
            current_app.logger.error(f"Docker daemon connectivity failed: {e}")
            return {"error": "Failed to connect to Docker daemon. Check Docker socket permissions.", "success": False}, 500
        
        # Execute the actual command
        timeout = current_app.config.get('DOCKER_TIMEOUT', 30)
        current_app.logger.info(f"Executing Docker command: {command}")
        
        # Use shell=True for Windows compatibility, but be careful with command injection
        if isinstance(command, list):
            result = subprocess.run(command, capture_output=True, text=True, timeout=timeout)
        else:
            result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=timeout)
        
        current_app.logger.info(f"Docker command completed with return code: {result.returncode}")
        
        if result.returncode == 0:
            return {"success": True, "output": result.stdout.strip()}, 200
        else:
            current_app.logger.error(f"Docker command failed: {result.stderr.strip()}")
            return {"success": False, "error": result.stderr.strip()}, 400
    except subprocess.TimeoutExpired:
        current_app.logger.error("Docker command timed out")
        return {"error": "Command timed out", "success": False}, 408
    except Exception as e:
        current_app.logger.error(f"Unexpected error executing Docker command: {e}")
        return {"error": str(e), "success": False}, 500
