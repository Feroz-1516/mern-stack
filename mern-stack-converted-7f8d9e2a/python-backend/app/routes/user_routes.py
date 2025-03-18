from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.models.user import User
from app import db
from flasgger import swag_from

user_routes = Blueprint('user_routes', __name__)

@user_routes.route('/signup', methods=['POST'])
@swag_from({
    'tags': ['Users'],
    'description': 'Register a new user',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'schema': {
                'type': 'object',
                'properties': {
                    'name': {'type': 'string'},
                    'email': {'type': 'string'},
                    'password': {'type': 'string'}
                },
                'required': ['name', 'email', 'password']
            }
        }
    ],
    'responses': {
        201: {
            'description': 'User created successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'user': {
                        'type': 'object',
                        'properties': {
                            'id': {'type': 'integer'},
                            'name': {'type': 'string'},
                            'email': {'type': 'string'}
                        }
                    }
                }
            }
        },
        400: {
            'description': 'Bad request'
        },
        500: {
            'description': 'Internal server error'
        }
    }
})
def sign_up():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if not all([name, email, password]):
        return jsonify({'message': 'All fields are required'}), 400

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({'message': 'User already exists!'}), 400

    new_user = User(name=name, email=email)
    new_user.set_password(password)

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'user': new_user.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error creating user', 'error': str(e)}), 500

@user_routes.route('/login', methods=['POST'])
@swag_from({
    'tags': ['Users'],
    'description': 'User login',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'schema': {
                'type': 'object',
                'properties': {
                    'email': {'type': 'string'},
                    'password': {'type': 'string'}
                },
                'required': ['email', 'password']
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Login successful',
            'schema': {
                'type': 'object',
                'properties': {
                    'user': {
                        'type': 'object',
                        'properties': {
                            'id': {'type': 'integer'},
                            'name': {'type': 'string'},
                            'email': {'type': 'string'}
                        }
                    },
                    'access_token': {'type': 'string'}
                }
            }
        },
        400: {
            'description': 'Bad request'
        },
        404: {
            'description': 'User not found'
        },
        500: {
            'description': 'Internal server error'
        }
    }
})
def log_in():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not all([email, password]):
        return jsonify({'message': 'Email and password are required'}), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'message': 'User not found'}), 404

    if user.check_password(password):
        access_token = create_access_token(identity=user.id)
        return jsonify({'user': user.to_dict(), 'access_token': access_token}), 200
    else:
        return jsonify({'message': 'Incorrect password!'}), 400

@user_routes.route('/users', methods=['GET'])
@jwt_required()
@swag_from({
    'tags': ['Users'],
    'description': 'Get all users',
    'responses': {
        200: {
            'description': 'List of all users',
            'schema': {
                'type': 'object',
                'properties': {
                    'users': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'id': {'type': 'integer'},
                                'name': {'type': 'string'},
                                'email': {'type': 'string'}
                            }
                        }
                    }
                }
            }
        },
        500: {
            'description': 'Internal server error'
        }
    }
})
def get_all_users():
    try:
        users = User.query.all()
        return jsonify({'users': [user.to_dict() for user in users]}), 200
    except Exception as e:
        return jsonify({'message': 'Error fetching users', 'error': str(e)}), 500

# Add error handlers for JWT-related issues
@user_routes.errorhandler(jwt_required)
def handle_auth_error(e):
    return jsonify({'message': 'Access token is missing or invalid'}), 401