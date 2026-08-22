
# backend/config.py
"""
Configuration for Flask Application
Educational Phishing Detection Simulator
"""

import os
from pathlib import Path
from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parent.parent

class Config:
    """Base configuration"""
    
    # App settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    
    # Database
    DATABASE_PATH = os.getenv('DATABASE_PATH', str(BASE_DIR / 'database' / 'phishing_simulator.db'))
    
    # ML Model
    ML_MODEL_PATH = os.getenv('ML_MODEL_PATH', str(BASE_DIR / 'ml' / 'model' / 'phishing_model.pkl'))
    
    # Security
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    
    # CORS
    CORS_ORIGINS = ['http://localhost:5000', 'http://127.0.0.1:5000']
    
    # Rate limiting (requests per minute)
    RATE_LIMIT = 60

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}