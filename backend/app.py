# backend/app.py
"""
Main Flask Application
Educational Phishing Detection Simulator
"""

from flask import Flask, render_template, send_from_directory
from flask_cors import CORS
from backend.config import config
from backend.database.db_manager import DatabaseManager
import os

def create_app(config_name='default'):
    """Create and configure Flask application"""
    
    app = Flask(__name__,
                template_folder='../frontend',
                static_folder='../frontend')
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Enable CORS
    CORS(app, origins=app.config['CORS_ORIGINS'])
    
    # Initialize database
    db = DatabaseManager(app.config['DATABASE_PATH'])
    
    # Register routes
    from backend.routes import register_routes
    register_routes(app)
    
    # Root route
    @app.route('/')
    def index():
        """Landing page"""
        return send_from_directory(app.static_folder, 'index.html')
    
    # Serve static HTML pages
    @app.route('/<path:filename>')
    def serve_page(filename):
        """Serve HTML pages"""
        if filename.endswith('.html'):
            return send_from_directory(app.static_folder, filename)
        return send_from_directory(app.static_folder, filename)
    
    # Health check
    @app.route('/health')
    def health():
        """Health check endpoint"""
        return {'status': 'healthy', 'app': 'Phishing Detection Simulator'}, 200
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(e):
        """404 error handler"""
        return {'error': 'Resource not found'}, 404
    
    @app.errorhandler(500)
    def server_error(e):
        """500 error handler"""
        return {'error': 'Internal server error'}, 500
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
    