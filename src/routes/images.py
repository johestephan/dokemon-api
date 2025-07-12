#!/usr/bin/env python3

from flask import Blueprint, jsonify, request
from utils.docker_utils import run_docker_command
from utils.parsers import parse_image_list

# Create blueprint for image management
images_bp = Blueprint('images', __name__, url_prefix='/api/v1/images')

@images_bp.route('', methods=['GET'])
def list_images():
    """List all images"""
    command = "docker images"
    response, status = run_docker_command(command)
    
    if status == 200:
        images = parse_image_list(response["output"])
        return jsonify({"images": images})
    else:
        return jsonify(response), status

@images_bp.route('/pull', methods=['POST'])
def pull_image():
    """Pull an image"""
    data = request.get_json()
    if not data or 'image' not in data:
        return jsonify({"error": "Image name is required"}), 400
    
    image = data['image']
    command = f"docker pull {image}"
    response, status = run_docker_command(command)
    return jsonify(response), status

@images_bp.route('/<image_id>/remove', methods=['DELETE'])
def remove_image(image_id):
    """Remove an image"""
    force = request.args.get('force', 'false').lower() == 'true'
    command = f"docker rmi {'--force' if force else ''} {image_id}"
    response, status = run_docker_command(command)
    return jsonify(response), status

@images_bp.route('/build', methods=['POST'])
def build_image():
    """Build an image from Dockerfile"""
    data = request.get_json()
    if not data or 'tag' not in data:
        return jsonify({"error": "Tag is required"}), 400
    
    tag = data['tag']
    path = data.get('path', '.')
    dockerfile = data.get('dockerfile', 'Dockerfile')
    
    command = f"docker build -t {tag} -f {dockerfile} {path}"
    response, status = run_docker_command(command)
    return jsonify(response), status
