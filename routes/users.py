#!/usr/bin/env python3

from datetime import datetime
from flask import Blueprint, jsonify, request, session, Response
from utils.auth_db import (
    create_user, authenticate_user, change_user_password, 
    get_current_user, get_user_info, require_auth, require_admin, 
    create_default_admin, list_users, deactivate_user, activate_user, 
    delete_user, is_admin_user
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
    
    # Get additional user info from database
    user_info = get_user_info(username)
    
    if user_info:
        return jsonify({
            "success": True,
            "user": {
                "username": username,
                "email": user_info.get('email'),
                "created_at": user_info.get('created_at'),
                "last_login": user_info.get('last_login'),
                "login_time": login_time,
                "authenticated": True,
                "is_admin": user_info.get('is_admin', False)
            }
        }), 200
    else:
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
    create_default_admin()

# Admin endpoints for user management
@users_bp.route('/list', methods=['GET'])
@require_admin
def list_all_users():
    """List all users (admin only)"""
    users = list_users()
    
    return jsonify({
        "success": True,
        "users": users,
        "count": len(users)
    }), 200

@users_bp.route('/<username>/info', methods=['GET'])
@require_admin
def get_user_details(username):
    """Get detailed user information (admin only)"""
    user_info = get_user_info(username)
    
    if user_info:
        return jsonify({
            "success": True,
            "user": user_info
        }), 200
    else:
        return jsonify({
            "success": False,
            "error": "User not found"
        }), 404

@users_bp.route('/<username>/deactivate', methods=['POST'])
@require_admin
def deactivate_user_account(username):
    """Deactivate a user account (admin only)"""
    current_user = get_current_user()
    
    # Prevent admin from deactivating themselves
    if username == current_user:
        return jsonify({
            "success": False,
            "error": "Cannot deactivate your own account"
        }), 400
    
    success, message = deactivate_user(username)
    
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

@users_bp.route('/<username>/activate', methods=['POST'])
@require_admin
def activate_user_account(username):
    """Activate a user account (admin only)"""
    success, message = activate_user(username)
    
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

@users_bp.route('/<username>/delete', methods=['DELETE'])
@require_admin
def delete_user_account(username):
    """Delete a user account (admin only)"""
    current_user = get_current_user()
    
    # Prevent admin from deleting themselves
    if username == current_user:
        return jsonify({
            "success": False,
            "error": "Cannot delete your own account"
        }), 400
    
    success, message = delete_user(username)
    
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

@users_bp.route('/<username>/reset-password', methods=['POST'])
@require_admin
def admin_reset_password(username):
    """Reset user password (admin only)"""
    data = request.get_json()
    if not data:
        return jsonify({"error": "JSON data required"}), 400
    
    new_password = data.get('newPassword')
    
    if not new_password:
        return jsonify({"error": "New password is required"}), 400
    
    if len(new_password) < 8:
        return jsonify({"error": "Password must be at least 8 characters"}), 400
    
    # For admin reset, we bypass the old password check
    # This is a security-sensitive operation, so we use the database directly
    try:
        from utils.auth_db import hash_password, get_db_connection
        password_data = hash_password(new_password)
        
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE users 
                SET password_hash = ?, salt = ?, password_changed_at = ?
                WHERE username = ?
            ''', (
                password_data['hash'],
                password_data['salt'],
                datetime.utcnow().isoformat(),
                username
            ))
            
            if cursor.rowcount > 0:
                conn.commit()
                return jsonify({
                    "success": True,
                    "message": "Password reset successfully"
                }), 200
            else:
                return jsonify({
                    "success": False,
                    "error": "User not found"
                }), 404
                
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Failed to reset password: {str(e)}"
        }), 500

@users_bp.route('/admin/promote/<username>', methods=['POST'])
@require_admin
def promote_to_admin(username):
    """Promote a user to admin (admin only)"""
    try:
        from utils.auth_db import get_db_connection
        
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE users 
                SET is_admin = 1 
                WHERE username = ? AND active = 1
            ''', (username,))
            
            if cursor.rowcount > 0:
                conn.commit()
                return jsonify({
                    "success": True,
                    "message": f"User {username} promoted to admin"
                }), 200
            else:
                return jsonify({
                    "success": False,
                    "error": "User not found or inactive"
                }), 404
                
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Failed to promote user: {str(e)}"
        }), 500

@users_bp.route('/admin/demote/<username>', methods=['POST'])
@require_admin
def demote_from_admin(username):
    """Demote a user from admin (admin only)"""
    current_user = get_current_user()
    
    # Prevent admin from demoting themselves
    if username == current_user:
        return jsonify({
            "success": False,
            "error": "Cannot demote yourself from admin"
        }), 400
    
    try:
        from utils.auth_db import get_db_connection
        
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Check if this is the last admin user
            cursor.execute("SELECT COUNT(*) as count FROM users WHERE is_admin = 1 AND active = 1")
            admin_count = cursor.fetchone()['count']
            
            if admin_count <= 1:
                return jsonify({
                    "success": False,
                    "error": "Cannot demote the last admin user"
                }), 400
            
            cursor.execute('''
                UPDATE users 
                SET is_admin = 0 
                WHERE username = ?
            ''', (username,))
            
            if cursor.rowcount > 0:
                conn.commit()
                return jsonify({
                    "success": True,
                    "message": f"User {username} demoted from admin"
                }), 200
            else:
                return jsonify({
                    "success": False,
                    "error": "User not found"
                }), 404
                
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Failed to demote user: {str(e)}"
        }), 500
