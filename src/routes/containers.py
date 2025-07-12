#!/usr/bin/env python3

from flask import Blueprint, jsonify, request
import json
from utils.docker_utils import run_docker_command
from utils.parsers import parse_container_list

# Create blueprint for container management
containers_bp = Blueprint('containers', __name__, url_prefix='/api/v1/containers')

@containers_bp.route('', methods=['GET'])
def list_containers():
    """List all containers"""
    show_all = request.args.get('all', 'false').lower() == 'true'
    command = "docker ps -a" if show_all else "docker ps"
    
    response, status = run_docker_command(command)
    if status == 200:
        containers = parse_container_list(response["output"])
        return jsonify({"containers": containers})
    else:
        return jsonify(response), status

@containers_bp.route('/<container_id>/start', methods=['POST'])
def start_container(container_id):
    """Start a container"""
    command = f"docker start {container_id}"
    response, status = run_docker_command(command)
    return jsonify(response), status

@containers_bp.route('/<container_id>/stop', methods=['POST'])
def stop_container(container_id):
    """Stop a container"""
    command = f"docker stop {container_id}"
    response, status = run_docker_command(command)
    return jsonify(response), status

@containers_bp.route('/<container_id>/restart', methods=['POST'])
def restart_container(container_id):
    """Restart a container"""
    command = f"docker restart {container_id}"
    response, status = run_docker_command(command)
    return jsonify(response), status

@containers_bp.route('/<container_id>/remove', methods=['DELETE'])
def remove_container(container_id):
    """Remove a container"""
    force = request.args.get('force', 'false').lower() == 'true'
    command = f"docker rm {'--force' if force else ''} {container_id}"
    response, status = run_docker_command(command)
    return jsonify(response), status

@containers_bp.route('/<container_id>/logs', methods=['GET'])
def get_container_logs(container_id):
    """Get container logs"""
    follow = request.args.get('follow', 'false').lower() == 'true'
    tail = request.args.get('tail', '100')
    
    if follow:
        return jsonify({"error": "Follow mode not supported in REST API"}), 400
    
    command = f"docker logs --tail {tail} {container_id}"
    response, status = run_docker_command(command)
    return jsonify(response), status

@containers_bp.route('/<container_id>/inspect', methods=['GET'])
def inspect_container(container_id):
    """Inspect a container"""
    command = f"docker inspect {container_id}"
    response, status = run_docker_command(command)
    
    if status == 200:
        try:
            # Parse JSON output from docker inspect
            inspect_data = json.loads(response["output"])
            return jsonify({"container_info": inspect_data})
        except json.JSONDecodeError:
            return jsonify({"error": "Failed to parse container info"}), 500
    else:
        return jsonify(response), status

@containers_bp.route('/<container_id>/exec', methods=['POST'])
def exec_in_container(container_id):
    """Execute a command in a container"""
    data = request.get_json()
    if not data or 'command' not in data:
        return jsonify({"error": "Command is required"}), 400
    
    cmd = data['command']
    interactive = data.get('interactive', False)
    
    if interactive:
        return jsonify({"error": "Interactive mode not supported in REST API"}), 400
    
    command = f"docker exec {container_id} {cmd}"
    response, status = run_docker_command(command)
    return jsonify(response), status

@containers_bp.route('/run', methods=['POST'])
def run_container():
    """Run a new container"""
    data = request.get_json()
    if not data or 'image' not in data:
        return jsonify({"error": "Image name is required"}), 400
    
    image = data['image']
    name = data.get('name', '')
    detached = data.get('detached', True)
    ports = data.get('ports', [])
    volumes = data.get('volumes', [])
    environment = data.get('environment', [])
    command_args = data.get('command', '')
    
    # Build docker run command
    docker_cmd = "docker run"
    
    if detached:
        docker_cmd += " -d"
    
    if name:
        docker_cmd += f" --name {name}"
    
    # Add port mappings
    for port in ports:
        if ':' in port:
            docker_cmd += f" -p {port}"
        else:
            docker_cmd += f" -p {port}:{port}"
    
    # Add volume mounts
    for volume in volumes:
        docker_cmd += f" -v {volume}"
    
    # Add environment variables
    for env in environment:
        docker_cmd += f" -e {env}"
    
    docker_cmd += f" {image}"
    
    if command_args:
        docker_cmd += f" {command_args}"
    
    response, status = run_docker_command(docker_cmd)
    return jsonify(response), status
