from flask import Blueprint, request, jsonify
from app.models.user import User
from app.config.db import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token

user_controller = Blueprint('user_controller', __name__)

@user_controller.route('/users', methods=['GET'])
def get_all_users():
    try:
        users = User.query.all()
        return jsonify([user.to_dict() for user in users]), 200
    except Exception as e:
        return jsonify({"message": "Error fetching users", "error": str(e)}), 500

@user_controller.route('/signup', methods=['POST'])
def sign_up():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if not all([name, email, password]):
        return jsonify({"message": "All fields are required"}), 400

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"message": "User already exists!"}), 400

    hashed_password = generate_password_hash(password)
    new_user = User(name=name, email=email, password=hashed_password)

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify(new_user.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error creating user", "error": str(e)}), 500

@user_controller.route('/login', methods=['POST'])
def log_in():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not all([email, password]):
        return jsonify({"message": "Email and password are required"}), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"message": "User not found"}), 404

    if check_password_hash(user.password, password):
        access_token = create_access_token(identity=user.id)
        return jsonify({"user": user.to_dict(), "access_token": access_token}), 200
    else:
        return jsonify({"message": "Incorrect password!"}), 400