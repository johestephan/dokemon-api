#!/usr/bin/env python3

from flask import Blueprint, jsonify, request
from utils.docker_utils import run_docker_command
from utils.parsers import parse_network_list

# Create blueprint for network management
networks_bp = Blueprint('networks', __name__, url_prefix='/api/v1/networks')

@networks_bp.route('', methods=['GET'])
def list_networks():
    """List all networks"""
    command = "docker network ls"
    response, status = run_docker_command(command)
    
    if status == 200:
        networks = parse_network_list(response["output"])
        return jsonify({"networks": networks})
    else:
        return jsonify(response), status

@networks_bp.route('/create', methods=['POST'])
def create_network():
    """Create a network"""
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({"error": "Network name is required"}), 400
    
    name = data['name']
    driver = data.get('driver', 'bridge')
    
    command = f"docker network create --driver {driver} {name}"
    response, status = run_docker_command(command)
    return jsonify(response), status

@networks_bp.route('/<network_name>/remove', methods=['DELETE'])
def remove_network(network_name):
    """Remove a network"""
    command = f"docker network rm {network_name}"
    response, status = run_docker_command(command)
    return jsonify(response), status
