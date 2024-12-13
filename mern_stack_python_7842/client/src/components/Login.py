import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from config import Config

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)
jwt = JWTManager(app)

@app.route('/api/users/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    # Here you would typically check the user credentials against your database
    # For demonstration, we'll use a mock user
    if email == "test@example.com" and password == "password":
        access_token = create_access_token(identity=email)
        return jsonify(access_token=access_token, user_id="mock_user_id"), 200
    else:
        return jsonify({"msg": "Bad username or password"}), 401

@app.route('/api/users/signup', methods=['POST'])
def signup():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    # Here you would typically create a new user in your database
    # For demonstration, we'll just return a success message
    hashed_password = generate_password_hash(password)
    # Save user to database (not implemented in this example)
    
    access_token = create_access_token(identity=email)
    return jsonify(access_token=access_token, user_id="new_user_id"), 201

@app.route('/api/blogs', methods=['GET'])
@jwt_required()
def get_blogs():
    # This would typically fetch blogs from your database
    # For demonstration, we'll return a mock blog
    current_user = get_jwt_identity()
    mock_blog = {
        "id": "1",
        "title": "Sample Blog",
        "content": "This is a sample blog post.",
        "author": current_user
    }
    return jsonify([mock_blog]), 200

if __name__ == '__main__':
    app.run(debug=True)