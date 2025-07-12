#!/usr/bin/env python3

from flask import Blueprint, jsonify, request
from utils.docker_utils import run_docker_command
from utils.parsers import parse_volume_list

# Create blueprint for volume management
volumes_bp = Blueprint('volumes', __name__, url_prefix='/api/v1/volumes')

@volumes_bp.route('', methods=['GET'])
def list_volumes():
    """List all volumes"""
    command = "docker volume ls"
    response, status = run_docker_command(command)
    
    if status == 200:
        volumes = parse_volume_list(response["output"])
        return jsonify({"volumes": volumes})
    else:
        return jsonify(response), status

@volumes_bp.route('/create', methods=['POST'])
def create_volume():
    """Create a volume"""
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({"error": "Volume name is required"}), 400
    
    name = data['name']
    command = f"docker volume create {name}"
    response, status = run_docker_command(command)
    return jsonify(response), status

@volumes_bp.route('/<volume_name>/remove', methods=['DELETE'])
def remove_volume(volume_name):
    """Remove a volume"""
    command = f"docker volume rm {volume_name}"
    response, status = run_docker_command(command)
    return jsonify(response), status
