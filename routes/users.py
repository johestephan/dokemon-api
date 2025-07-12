#!/usr/bin/env python3

from datetime import datetime
from flask import Blueprint, jsonify, request, session, Response, Response
from utils.auth import (
    create_user, authenticate_user, change_user_password, 
    get_current_user, require_auth, create_default_admin
)

# Create blueprint for user management
users_bp = Blueprint('users', __name__, url_prefix='/api/v1/users')

@users_bp.route('', methods=['POST'])
def create_new_user():
    """Create a new user"""
    data = request.get_json()
    if not data:
        return jsonify({"error": "JSON data required"}), 400
    
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    
    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400
    
    success, message = create_user(username, password, email)
    
    if success:
        return jsonify({
            "success": True,
            "message": message,
            "username": username
        }), 201
    else:
        return jsonify({
            "success": False,
            "error": message
        }), 400

@users_bp.route('/login', methods=['POST'])
def login():
    """User login - sets authentication cookie/session"""
    data = request.get_json()
    if not data:
        return jsonify({"error": "JSON data required"}), 400
    
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400
    
    success, message = authenticate_user(username, password)
    
    if success:
        # Set session data
        session['username'] = username
        session['login_time'] = datetime.utcnow().isoformat()
        session.permanent = True  # Make session persistent
        
        return jsonify({
            "success": True,
            "message": message,
            "username": username
        }), 200
    else:
        return jsonify({
            "success": False,
            "error": message
        }), 401

@users_bp.route('/logout', methods=['POST'])
def logout():
    """User logout - clears authentication cookie/session"""
    username = get_current_user()
    
    # Clear session
    session.clear()
    
    return jsonify({
        "success": True,
        "message": "Logged out successfully",
        "username": username
    }), 200

@users_bp.route('/logout', methods=['GET'])
def logout_page():
    """User logout page - returns HTML page and clears session"""
    username = get_current_user()
    
    # Clear session
    session.clear()
    
    # Return HTML page
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Dokémon NG</title>
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                margin: 0;
                padding: 0;
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            .container {
                background: white;
                padding: 2rem;
                border-radius: 10px;
                box-shadow: 0 10px 25px rgba(0,0,0,0.1);
                text-align: center;
                max-width: 400px;
                width: 90%;
            }
            .logo {
                font-size: 2.5rem;
                font-weight: bold;
                color: #667eea;
                margin-bottom: 1rem;
            }
            .message {
                color: #28a745;
                font-size: 1.2rem;
                margin-bottom: 1.5rem;
            }
            .info {
                color: #6c757d;
                margin-bottom: 2rem;
            }
            .api-info {
                background: #f8f9fa;
                padding: 1rem;
                border-radius: 5px;
                margin-top: 2rem;
                font-size: 0.9rem;
                color: #495057;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="logo">🐾 Dokémon NG</div>
            <div class="message">✅ Logout Successful</div>
            <div class="info">You have been successfully logged out from the Dokemon API.</div>
            
            <div class="api-info">
                <strong>Dokemon API</strong><br>
                Docker Management Interface<br>
                Session cleared successfully
            </div>
        </div>
    </body>
    </html>
    """
    
    return Response(html_content, mimetype='text/html'), 200

@users_bp.route('/me', methods=['GET'])
@require_auth
def get_current_user_info():
    """Get current user information"""
    username = get_current_user()
    login_time = session.get('login_time')
    
    return jsonify({
        "success": True,
        "user": {
            "username": username,
            "login_time": login_time,
            "authenticated": True
        }
    }), 200

# Add change password endpoint at the blueprint level
@users_bp.route('/changepassword', methods=['POST'])
@require_auth
def change_password():
    """Change user password"""
    data = request.get_json()
    if not data:
        return jsonify({"error": "JSON data required"}), 400
    
    current_password = data.get('currentPassword')
    new_password = data.get('newPassword')
    
    if not current_password or not new_password:
        return jsonify({"error": "Current password and new password are required"}), 400
    
    username = get_current_user()
    success, message = change_user_password(username, current_password, new_password)
    
    if success:
        return jsonify({
            "success": True,
            "message": message
        }), 200
    else:
        return jsonify({
            "success": False,
            "error": message
        }), 400

# Initialize default admin user when blueprint is created
def init_users():
    """Initialize user system with default admin if needed"""
    from datetime import datetime
    create_default_admin()
