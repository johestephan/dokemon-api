#!/usr/bin/env python3

import os

class Config:
    """Dokemon API Configuration"""
    
    # Server configuration
    HOST = os.environ.get('DOKEMON_HOST', '0.0.0.0')
    PORT = int(os.environ.get('DOKEMON_PORT', 9090))
    DEBUG = os.environ.get('DOKEMON_DEBUG', 'True').lower() == 'true'
    
    # API configuration
    API_VERSION = '1.0.0'
    API_NAME = 'Dokemon API'
    API_DESCRIPTION = 'A RESTful API for Docker management'
    
    # Docker configuration
    DOCKER_TIMEOUT = int(os.environ.get('DOKEMON_DOCKER_TIMEOUT', 30))
    DOCKER_VERSION_TIMEOUT = int(os.environ.get('DOKEMON_VERSION_TIMEOUT', 5))
    
    # Security configuration
    ALLOWED_HOSTS = os.environ.get('DOKEMON_ALLOWED_HOSTS', '*').split(',')
    
    # Logging configuration
    LOG_LEVEL = os.environ.get('DOKEMON_LOG_LEVEL', 'INFO')
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

class DevelopmentConfig(Config):
    DEBUG = True
    
class ProductionConfig(Config):
    DEBUG = False

# Configuration mapping
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
