#!/usr/bin/env python3
"""
Standalone database initialization script for Dokemon API
Creates the SQLite database and tables without Flask dependencies
Compatible with Python 2.7+ and Python 3.x

This script should be run from the project root directory.
"""

import sqlite3
import hashlib
import os
try:
    import secrets
except ImportError:
    # Fallback for older Python versions
    secrets = None
from datetime import datetime

# Database configuration - matches the structure used by the application
DATABASE_FILE = 'data/dokemon.db'
DATABASE_DIR = 'data'

def hash_password(password, salt=None):
    """Hash a password with salt using PBKDF2"""
    if salt is None:
        # Use secrets if available (Python 3.6+), otherwise use os.urandom
        try:
            salt = secrets.token_hex(16)
        except (ImportError, AttributeError):
            import binascii
            salt = binascii.hexlify(os.urandom(16)).decode('ascii')
    
    # Create password hash using salt + password (100,000 iterations for security)
    password_hash = hashlib.pbkdf2_hmac('sha256', 
                                       password.encode('utf-8'), 
                                       salt.encode('utf-8'), 
                                       100000)
    
    return {
        'hash': password_hash.hex(),
        'salt': salt
    }

def init_database():
    """Initialize the database and create tables if they don't exist"""
    # Ensure data directory exists
    if not os.path.exists(DATABASE_DIR):
        os.makedirs(DATABASE_DIR)
        print("Created data directory: " + DATABASE_DIR)
    
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
    print("Created 'users' table")
    
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
    print("Created 'user_sessions' table")
    
    conn.commit()
    conn.close()
    print("Database initialized: " + DATABASE_FILE)

def create_default_admin(username='admin', password='admin', email='admin@dokemon.local'):
    """Create default admin user if no admin users exist"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    # Check if any admin users exist
    cursor.execute("SELECT COUNT(*) as count FROM users WHERE is_admin = 1")
    admin_count = cursor.fetchone()[0]
    
    if admin_count == 0:
        # Check if username already exists
        cursor.execute("SELECT username FROM users WHERE username = ?", (username,))
        if cursor.fetchone():
            print("User '" + username + "' already exists")
            conn.close()
            return False
        
        # Hash password
        password_data = hash_password(password)
        
        # Insert new admin user
        cursor.execute('''
            INSERT INTO users (username, password_hash, salt, email, created_at, is_admin)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            username,
            password_data['hash'],
            password_data['salt'],
            email,
            datetime.utcnow().isoformat(),
            1  # is_admin = True
        ))
        
        conn.commit()
        print("✅ Default admin user created: " + username + " / " + password)
        print("⚠️  IMPORTANT: Please change the password immediately!")
        conn.close()
        return True
    else:
        print("Admin users already exist (" + str(admin_count) + " found)")
        conn.close()
        return True

def list_users():
    """List all users in the database"""
    if not os.path.exists(DATABASE_FILE):
        print("Database does not exist yet")
        return
    
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row  # Enable dict-like access
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT username, email, created_at, last_login, active, is_admin
        FROM users 
        ORDER BY created_at
    ''')
    
    users = cursor.fetchall()
    
    if users:
        print("\n📋 Current Users:")
        print("-" * 80)
        print("%-15s %-25s %-8s %-8s %s" % ('Username', 'Email', 'Admin', 'Active', 'Created'))
        print("-" * 80)
        
        for user in users:
            admin_status = "Yes" if user['is_admin'] else "No"
            active_status = "Yes" if user['active'] else "No"
            created = user['created_at'][:19] if user['created_at'] else "Unknown"
            email = user['email'] if user['email'] else 'N/A'
            
            print("%-15s %-25s %-8s %-8s %s" % (user['username'], email, admin_status, active_status, created))
    else:
        print("No users found in database")
    
    conn.close()

def verify_database():
    """Verify database structure and content"""
    if not os.path.exists(DATABASE_FILE):
        print("❌ Database file does not exist")
        return False
    
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    # Check tables exist
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cursor.fetchall()]
    
    print("✅ Database file exists: " + DATABASE_FILE)
    print("✅ Tables found: " + ', '.join(tables))
    
    # Check users table structure
    cursor.execute("PRAGMA table_info(users)")
    columns = cursor.fetchall()
    
    print("✅ Users table structure:")
    for col in columns:
        print("   - " + col[1] + " (" + col[2] + ")")
    
    # Count users
    cursor.execute("SELECT COUNT(*) FROM users")
    user_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM users WHERE is_admin = 1")
    admin_count = cursor.fetchone()[0]
    
    print("✅ Total users: " + str(user_count))
    print("✅ Admin users: " + str(admin_count))
    
    conn.close()
    return True

if __name__ == "__main__":
    print("🚀 Dokemon API Database Initialization")
    print("=" * 50)
    
    # Initialize database
    init_database()
    
    # Create default admin
    create_default_admin()
    
    # Verify everything worked
    print("\n🔍 Database Verification:")
    verify_database()
    
    # List users
    list_users()
    
    print("\n✅ Database setup complete!")
    print("📁 Database location: " + os.path.abspath(DATABASE_FILE))
