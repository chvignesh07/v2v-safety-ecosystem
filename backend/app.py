"""Flask Application for V2V Safety Ecosystem Backend

This module serves as the main application entry point for the V2V Safety Ecosystem backend.
It sets up Flask with SocketIO for real-time communication, initializes the application
with necessary blueprints and configurations.

Author: V2V Safety Team
Date: September 7, 2025
Version: 1.0.0
"""

from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS
import os
import logging
from datetime import datetime

# Import blueprints (will be created later)
from api.routes import api_bp
from api.health import health_bp
from socketio_handlers import init_socketio

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_app(config_name='development'):
    """Application factory pattern for creating Flask app instances.
    
    Args:
        config_name (str): Configuration environment name
        
    Returns:
        Flask: Configured Flask application instance
    """
    app = Flask(__name__)
    
    # Load configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['DEBUG'] = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    app.config['HOST'] = os.environ.get('FLASK_HOST', '0.0.0.0')
    app.config['PORT'] = int(os.environ.get('FLASK_PORT', 5000))
    
    # Initialize extensions
    CORS(app, resources={
        r"/api/*": {
            "origins": ["http://localhost:3000", "http://localhost:8080"],
            "methods": ["GET", "POST", "PUT", "DELETE"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    
    # Register blueprints
    app.register_blueprint(health_bp, url_prefix='/health')
    app.register_blueprint(api_bp, url_prefix='/api')
    
    logger.info(f"Flask app created successfully in {config_name} mode")
    return app

def create_socketio_app():
    """Creates Flask-SocketIO application for real-time communication.
    
    Returns:
        tuple: (Flask app, SocketIO instance)
    """
    app = create_app()
    
    # Initialize SocketIO with CORS settings
    socketio = SocketIO(
        app,
        cors_allowed_origins=[
            "http://localhost:3000",
            "http://localhost:8080"
        ],
        async_mode='threading',
        logger=True,
        engineio_logger=True
    )
    
    # Initialize socket handlers
    init_socketio(socketio)
    
    logger.info("SocketIO initialized successfully")
    return app, socketio

if __name__ == '__main__':
    """Run the application in development mode."""
    logger.info("Starting V2V Safety Ecosystem Backend Server...")
    logger.info(f"Server started at: {datetime.now()}")
    
    # Create app with SocketIO
    app, socketio = create_socketio_app()
    
    # Run the application
    socketio.run(
        app,
        host=app.config['HOST'],
        port=app.config['PORT'],
        debug=app.config['DEBUG']
    )
