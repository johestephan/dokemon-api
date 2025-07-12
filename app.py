#!/usr/bin/env python3

from flask import Flask
import os
from config import config

# Import all route blueprints
from routes.health import health_bp
from routes.containers import containers_bp
from routes.images import images_bp
from routes.networks import networks_bp
from routes.volumes import volumes_bp
from routes.system import system_bp
from routes.users import users_bp

def create_app():
    """Application factory pattern"""
    app = Flask(__name__)
    
    # Load configuration
    env = os.environ.get('FLASK_ENV', 'default')
    app.config.from_object(config[env])
    
    # Set up session configuration for authentication
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dokemon-secret-key-change-in-production')
    app.config['PERMANENT_SESSION_LIFETIME'] = 7200  # 2 hours in seconds
    
    # Initialize authentication system
    from routes.users import init_users
    init_users()
    
    # Register all blueprints
    app.register_blueprint(health_bp)           # Health check and API docs at /health and /
    app.register_blueprint(containers_bp)       # Container management at /api/v1/containers
    app.register_blueprint(images_bp)           # Image management at /api/v1/images
    app.register_blueprint(networks_bp)         # Network management at /api/v1/networks
    app.register_blueprint(volumes_bp)          # Volume management at /api/v1/volumes
    app.register_blueprint(system_bp)           # System operations at /api/v1/system
    app.register_blueprint(users_bp)            # User management at /api/v1/users
    
    return app

def print_startup_info(app):
    """Print startup information for development server"""
    print(f"Starting {app.config.get('API_NAME', 'Dokemon API')} on port {app.config.get('PORT', 9090)}...")
    print("Docker Management API - A RESTful interface for Docker operations")
    print("Make sure Docker is running and accessible via /var/run/docker.sock")
    print(f"API Documentation available at: http://localhost:{app.config.get('PORT', 9090)}/")
    print("\n📁 Modular Structure:")
    print("   - Health & Documentation: /health, /")
    print("   - Containers: /api/v1/containers/*")
    print("   - Images: /api/v1/images/*")
    print("   - Networks: /api/v1/networks/*") 
    print("   - Volumes: /api/v1/volumes/*")
    print("   - System: /api/v1/system/*")
    print("   - Users: /api/v1/users/*")
    print("\n🔐 Authentication:")
    print("   - Create User: POST /api/v1/users")
    print("   - Login: POST /api/v1/users/login")
    print("   - Logout (JSON): POST /api/v1/users/logout")
    print("   - Logout (HTML): GET /api/v1/users/logout")
    print("   - Change Password: POST /api/v1/users/changepassword")
    print("   - Current User: GET /api/v1/users/me")
    print("\n👑 Admin Management:")
    print("   - List Users: GET /api/v1/users/list")
    print("   - User Info: GET /api/v1/users/<username>/info")
    print("   - Activate/Deactivate: POST /api/v1/users/<username>/activate|deactivate")
    print("   - Reset Password: POST /api/v1/users/<username>/reset-password")
    print("   - Promote/Demote Admin: POST /api/v1/users/admin/promote|demote/<username>")
    print("   - Delete User: DELETE /api/v1/users/<username>/delete")
    print("\n💾 Database: SQLite at data/dokemon.db (auto-created)")
    print("   Default admin user: admin/admin (change password immediately!)")

# Create the Flask application
app = create_app()

if __name__ == '__main__':
    # Only print startup messages in the main process, not the reloader
    if os.environ.get('WERKZEUG_RUN_MAIN') != 'true':
        print_startup_info(app)
    
    app.run(
        host=app.config.get('HOST', '0.0.0.0'), 
        port=app.config.get('PORT', 9090), 
        debug=app.config.get('DEBUG', True)
    )