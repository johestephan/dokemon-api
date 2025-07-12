#!/usr/bin/env python3

import sqlite3
import hashlib
import secrets
import os
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify, session
from contextlib import contextmanager

# Database configuration
DATABASE_FILE = 'data/dokemon.db'
DATABASE_DIR = 'data'

def init_database():
    """Initialize the database and create tables if they don't exist"""
    # Ensure data directory exists
    if not os.path.exists(DATABASE_DIR):
        os.makedirs(DATABASE_DIR)
    
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            salt TEXT NOT NULL,
            email TEXT,
            created_at TEXT NOT NULL,
            last_login TEXT,
            password_changed_at TEXT,
            active BOOLEAN NOT NULL DEFAULT 1,
            is_admin BOOLEAN NOT NULL DEFAULT 0
        )
    ''')
    
    # Create sessions table for better session management (optional enhancement)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            session_id TEXT UNIQUE NOT NULL,
            created_at TEXT NOT NULL,
            expires_at TEXT NOT NULL,
            active BOOLEAN NOT NULL DEFAULT 1,
            FOREIGN KEY (username) REFERENCES users (username)
        )
    ''')
    
    conn.commit()
    conn.close()

@contextmanager
def get_db_connection():
    """Context manager for database connections"""
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row  # Enable dict-like access to rows
    try:
        yield conn
    finally:
        conn.close()

def hash_password(password, salt=None):
    """Hash a password with salt using PBKDF2"""
    if salt is None:
        salt = secrets.token_hex(16)
    
    # Create password hash using salt + password (100,000 iterations for security)
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

def create_user(username, password, email=None, is_admin=False):
    """Create a new user in the database"""
    # Validate input
    if not username or len(username) < 3:
        return False, "Username must be at least 3 characters"
    
    if not password or len(password) < 8:
        return False, "Password must be at least 8 characters"
    
    # Hash password
    password_data = hash_password(password)
    
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Check if user already exists
            cursor.execute("SELECT username FROM users WHERE username = ?", (username,))
            if cursor.fetchone():
                return False, "User already exists"
            
            # Insert new user
            cursor.execute('''
                INSERT INTO users (username, password_hash, salt, email, created_at, is_admin)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                username,
                password_data['hash'],
                password_data['salt'],
                email,
                datetime.utcnow().isoformat(),
                is_admin
            ))
            
            conn.commit()
            return True, "User created successfully"
            
    except sqlite3.Error as e:
        return False, f"Database error: {str(e)}"

def authenticate_user(username, password):
    """Authenticate a user against the database"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Get user data
            cursor.execute('''
                SELECT username, password_hash, salt, active 
                FROM users 
                WHERE username = ?
            ''', (username,))
            
            user = cursor.fetchone()
            
            if not user:
                return False, "Invalid username or password"
            
            if not user['active']:
                return False, "Account is disabled"
            
            # Verify password
            if verify_password(password, user['password_hash'], user['salt']):
                # Update last login
                cursor.execute('''
                    UPDATE users 
                    SET last_login = ? 
                    WHERE username = ?
                ''', (datetime.utcnow().isoformat(), username))
                
                conn.commit()
                return True, "Authentication successful"
            else:
                return False, "Invalid username or password"
                
    except sqlite3.Error as e:
        return False, f"Database error: {str(e)}"

def change_user_password(username, old_password, new_password):
    """Change user password in the database"""
    # Validate new password
    if not new_password or len(new_password) < 8:
        return False, "New password must be at least 8 characters"
    
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Get current user data
            cursor.execute('''
                SELECT password_hash, salt 
                FROM users 
                WHERE username = ?
            ''', (username,))
            
            user = cursor.fetchone()
            
            if not user:
                return False, "User not found"
            
            # Verify old password
            if not verify_password(old_password, user['password_hash'], user['salt']):
                return False, "Current password is incorrect"
            
            # Hash new password
            password_data = hash_password(new_password)
            
            # Update password
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
            
            conn.commit()
            return True, "Password changed successfully"
            
    except sqlite3.Error as e:
        return False, f"Database error: {str(e)}"

def get_user_info(username):
    """Get user information from database"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT username, email, created_at, last_login, active, is_admin
                FROM users 
                WHERE username = ?
            ''', (username,))
            
            user = cursor.fetchone()
            
            if user:
                return dict(user)
            return None
            
    except sqlite3.Error as e:
        return None

def list_users(admin_only=False):
    """List all users (admin function)"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            if admin_only:
                cursor.execute('''
                    SELECT username, email, created_at, last_login, active, is_admin
                    FROM users 
                    WHERE is_admin = 1
                    ORDER BY created_at
                ''')
            else:
                cursor.execute('''
                    SELECT username, email, created_at, last_login, active, is_admin
                    FROM users 
                    ORDER BY created_at
                ''')
            
            users = cursor.fetchall()
            return [dict(user) for user in users]
            
    except sqlite3.Error as e:
        return []

def deactivate_user(username):
    """Deactivate a user account"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE users 
                SET active = 0 
                WHERE username = ?
            ''', (username,))
            
            if cursor.rowcount > 0:
                conn.commit()
                return True, "User deactivated successfully"
            else:
                return False, "User not found"
                
    except sqlite3.Error as e:
        return False, f"Database error: {str(e)}"

def activate_user(username):
    """Activate a user account"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE users 
                SET active = 1 
                WHERE username = ?
            ''', (username,))
            
            if cursor.rowcount > 0:
                conn.commit()
                return True, "User activated successfully"
            else:
                return False, "User not found"
                
    except sqlite3.Error as e:
        return False, f"Database error: {str(e)}"

def delete_user(username):
    """Delete a user from database (use with caution)"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Don't allow deleting the last admin user
            cursor.execute("SELECT COUNT(*) as count FROM users WHERE is_admin = 1")
            admin_count = cursor.fetchone()['count']
            
            cursor.execute("SELECT is_admin FROM users WHERE username = ?", (username,))
            user = cursor.fetchone()
            
            if user and user['is_admin'] and admin_count <= 1:
                return False, "Cannot delete the last admin user"
            
            cursor.execute("DELETE FROM users WHERE username = ?", (username,))
            
            if cursor.rowcount > 0:
                conn.commit()
                return True, "User deleted successfully"
            else:
                return False, "User not found"
                
    except sqlite3.Error as e:
        return False, f"Database error: {str(e)}"

# Session management functions
def get_current_user():
    """Get current logged-in user from session"""
    return session.get('username')

def is_authenticated():
    """Check if user is authenticated"""
    return 'username' in session and 'login_time' in session

def is_admin_user(username=None):
    """Check if user has admin privileges"""
    if username is None:
        username = get_current_user()
    
    if not username:
        return False
    
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT is_admin FROM users WHERE username = ? AND active = 1", (username,))
            user = cursor.fetchone()
            return user and user['is_admin']
    except sqlite3.Error:
        return False

def require_auth(f):
    """Decorator to require authentication for endpoints"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not is_authenticated():
            return jsonify({"error": "Authentication required"}), 401
        
        # Check session timeout (configurable) - default 2 hours
        login_time = session.get('login_time')
        if login_time:
            session_timeout = int(os.environ.get('SESSION_TIMEOUT_HOURS', 2))
            login_datetime = datetime.fromisoformat(login_time)
            if datetime.utcnow() - login_datetime > timedelta(hours=session_timeout):
                session.clear()
                return jsonify({"error": "Session expired"}), 401
        
        return f(*args, **kwargs)
    return decorated_function

def require_admin(f):
    """Decorator to require admin privileges for endpoints"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not is_authenticated():
            return jsonify({"error": "Authentication required"}), 401
        
        if not is_admin_user():
            return jsonify({"error": "Admin privileges required"}), 403
        
        return f(*args, **kwargs)
    return decorated_function

def create_default_admin(default_password='admin'):
    """Create default admin user if no admin users exist"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Check if any admin users exist
            cursor.execute("SELECT COUNT(*) as count FROM users WHERE is_admin = 1")
            admin_count = cursor.fetchone()['count']
            
            if admin_count == 0:
                # Create default admin user
                success, message = create_user('admin', default_password, 'admin@dokemon.local', is_admin=True)
                if success:
                    print(f"Default admin user created: admin / {default_password}")
                    print("IMPORTANT: Please change the password immediately!")
                return success
            return True
            
    except sqlite3.Error as e:
        print(f"Database error creating default admin: {str(e)}")
        return False

# Initialize database when module is imported
try:
    init_database()
except Exception as e:
    print(f"Warning: Database initialization failed: {str(e)}")
