#!/usr/bin/env python3

import hashlib
import secrets
import json
import os
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify, session

# Simple file-based user storage (for development - use database in production)
USERS_FILE = 'users.json'

def hash_password(password, salt=None):
    """Hash a password with salt"""
    if salt is None:
        salt = secrets.token_hex(16)
    
    # Create password hash using salt + password
    password_hash = hashlib.pbkdf2_hmac('sha256', 
                                       password.encode('utf-8'), 
                                       salt.encode('utf-8'), 
                                       100000)
    
    return {
        'hash': password_hash.hex(),
        'salt': salt
    }

def verify_password(password, stored_hash, salt):
    """Verify a password against stored hash"""
    password_data = hash_password(password, salt)
    return password_data['hash'] == stored_hash

def load_users():
    """Load users from file"""
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    return {}

def save_users(users):
    """Save users to file"""
    try:
        with open(USERS_FILE, 'w') as f:
            json.dump(users, f, indent=2)
        return True
    except IOError:
        return False

def create_user(username, password, email=None):
    """Create a new user"""
    users = load_users()
    
    # Check if user already exists
    if username in users:
        return False, "User already exists"
    
    # Validate username
    if not username or len(username) < 3:
        return False, "Username must be at least 3 characters"
    
    # Validate password
    if not password or len(password) < 8:
        return False, "Password must be at least 8 characters"
    
    # Hash password
    password_data = hash_password(password)
    
    # Create user record
    users[username] = {
        'password_hash': password_data['hash'],
        'salt': password_data['salt'],
        'email': email,
        'created_at': datetime.utcnow().isoformat(),
        'last_login': None,
        'active': True
    }
    
    # Save users
    if save_users(users):
        return True, "User created successfully"
    else:
        return False, "Failed to save user"

def authenticate_user(username, password):
    """Authenticate a user"""
    users = load_users()
    
    if username not in users:
        return False, "Invalid username or password"
    
    user = users[username]
    
    if not user.get('active', True):
        return False, "Account is disabled"
    
    # Verify password
    if verify_password(password, user['password_hash'], user['salt']):
        # Update last login
        user['last_login'] = datetime.utcnow().isoformat()
        save_users(users)
        return True, "Authentication successful"
    else:
        return False, "Invalid username or password"

def change_user_password(username, old_password, new_password):
    """Change user password"""
    users = load_users()
    
    if username not in users:
        return False, "User not found"
    
    user = users[username]
    
    # Verify old password
    if not verify_password(old_password, user['password_hash'], user['salt']):
        return False, "Current password is incorrect"
    
    # Validate new password
    if not new_password or len(new_password) < 8:
        return False, "New password must be at least 8 characters"
    
    # Hash new password
    password_data = hash_password(new_password)
    user['password_hash'] = password_data['hash']
    user['salt'] = password_data['salt']
    user['password_changed_at'] = datetime.utcnow().isoformat()
    
    # Save users
    if save_users(users):
        return True, "Password changed successfully"
    else:
        return False, "Failed to save password change"

def get_current_user():
    """Get current logged-in user from session"""
    return session.get('username')

def is_authenticated():
    """Check if user is authenticated"""
    return 'username' in session and 'login_time' in session

def require_auth(f):
    """Decorator to require authentication for endpoints"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not is_authenticated():
            return jsonify({"error": "Authentication required"}), 401
        
        # Check session timeout (optional) - default 24 hours
        login_time = session.get('login_time')
        if login_time:
            session_timeout = 24  # hours - can be made configurable later
            login_datetime = datetime.fromisoformat(login_time)
            if datetime.utcnow() - login_datetime > timedelta(hours=session_timeout):
                session.clear()
                return jsonify({"error": "Session expired"}), 401
        
        return f(*args, **kwargs)
    return decorated_function

def create_default_admin(default_password='admin'):
    """Create default admin user if no users exist"""
    users = load_users()
    if not users:
        # Create default admin user
        success, message = create_user('admin', default_password, 'admin@dokemon.local')
        if success:
            print(f"⚠️  Default admin user created: admin / {default_password}")
            print("⚠️  Please change the password immediately!")
        return success
    return True
