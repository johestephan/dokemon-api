#!/usr/bin/env python3

from flask import Blueprint, jsonify, request
from utils.docker_utils import run_docker_command
from utils.parsers import parse_docker_info

# Create blueprint for system operations
system_bp = Blueprint('system', __name__, url_prefix='/api/v1/system')

@system_bp.route('/info', methods=['GET'])
def system_info():
    """Get Docker system information"""
    command = "docker info"
    response, status = run_docker_command(command)
    
    if status == 200:
        try:
            # Parse the docker info output into structured data
            parsed_info = parse_docker_info(response["output"])
            return jsonify({
                "success": True,
                "system_info": parsed_info
            })
        except Exception as e:
            # Fallback to raw output if parsing fails
            return jsonify({
                "success": False,
                "error": f"Failed to parse system info: {str(e)}"
            }), 500
    else:
        return jsonify(response), status

@system_bp.route('/stats', methods=['GET'])
def system_stats():
    """Get container resource usage statistics"""
    no_stream = request.args.get('no-stream', 'true').lower() == 'true'
    command = f"docker stats {'--no-stream' if no_stream else ''}"
    response, status = run_docker_command(command)
    return jsonify(response), status

@system_bp.route('/prune', methods=['POST'])
def system_prune():
    """Clean up unused Docker objects"""
    force = request.args.get('force', 'false').lower() == 'true'
    command = f"docker system prune {'--force' if force else ''}"
    
    if not force:
        return jsonify({"error": "Force parameter required for safety"}), 400
    
    response, status = run_docker_command(command)
    return jsonify(response), status

@system_bp.route('/summary', methods=['GET'])
def system_summary():
    """Get Docker system summary with key statistics"""
    command = "docker info"
    response, status = run_docker_command(command)
    
    if status == 200:
        try:
            parsed_info = parse_docker_info(response["output"])
            
            # Extract key information for summary
            summary = {
                "docker_version": parsed_info.get("Server", {}).get("Server Version", "Unknown"),
                "containers": {
                    "total": parsed_info.get("Server", {}).get("Containers", 0),
                    "running": parsed_info.get("Server", {}).get("Running", 0),
                    "paused": parsed_info.get("Server", {}).get("Paused", 0),
                    "stopped": parsed_info.get("Server", {}).get("Stopped", 0)
                },
                "images": parsed_info.get("Server", {}).get("Images", 0),
                "storage_driver": parsed_info.get("Server", {}).get("Storage Driver", "Unknown"),
                "operating_system": parsed_info.get("Server", {}).get("Operating System", "Unknown"),
                "architecture": parsed_info.get("Server", {}).get("Architecture", "Unknown"),
                "cpus": parsed_info.get("Server", {}).get("CPUs", 0),
                "total_memory": parsed_info.get("Server", {}).get("Total Memory", "Unknown"),
                "kernel_version": parsed_info.get("Server", {}).get("Kernel Version", "Unknown")
            }
            
            return jsonify({
                "success": True,
                "summary": summary
            })
        except Exception as e:
            return jsonify({
                "success": False,
                "error": f"Failed to parse system info: {str(e)}"
            }), 500
    else:
        return jsonify(response), status
