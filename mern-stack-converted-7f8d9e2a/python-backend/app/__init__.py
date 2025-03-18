import os
from flask import Flask, jsonify
from flask_cors import CORS
from flasgger import Swagger
from flask_jwt_extended import JWTManager
from .config.db import init_db
from .routes.user_routes import user_routes
from .routes.blog_routes import blog_routes
import logging

def create_app():
    app = Flask(__name__)
    
    # Configure the app
    app.config.from_object('config.Config')
    
    # Set secret key from environment variable
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    
    # Set up logging
    logging.basicConfig(level=logging.INFO)
    
    # Initialize CORS
    CORS(app)
    
    # Initialize Swagger
    Swagger(app)
    
    # Initialize JWT
    JWTManager(app)
    
    # Initialize the database
    init_db()
    
    # Register blueprints
    app.register_blueprint(user_routes, url_prefix='/api/users')
    app.register_blueprint(blog_routes, url_prefix='/api/blogs')
    
    # Global error handler
    @app.errorhandler(Exception)
    def handle_error(error):
        logging.error(f"An error occurred: {str(error)}")
        return jsonify({"error": "An unexpected error occurred"}), 500
    
    return app