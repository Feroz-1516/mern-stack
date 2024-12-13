from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from werkzeug.security import generate_password_hash, check_password_hash
from ..model.user import User

api = Namespace('users', description='User operations')

user_model = api.model('User', {
    'name': fields.String(required=True, description='User name'),
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password'),
})

@api.route('/')
class UserList(Resource):
    @api.doc('list_users')
    @api.response(200, 'Success')
    @api.response(404, 'No users found')
    def get(self):
        """List all users"""
        try:
            users = User.objects.all()
        except Exception as e:
            api.logger.error(str(e))
            return {'message': 'An error occurred while fetching users'}, 500

        if not users:
            return {'message': 'Users are not found'}, 404

        return jsonify([user.to_dict() for user in users])

@api.route('/signup')
class SignUp(Resource):
    @api.doc('create_user')
    @api.expect(user_model)
    @api.response(201, 'User created successfully')
    @api.response(400, 'User already exists')
    def post(self):
        """Create a new user"""
        data = request.json
        name, email, password = data.get('name'), data.get('email'), data.get('password')

        try:
            existing_user = User.objects(email=email).first()
        except Exception as e:
            api.logger.error(str(e))
            return {'message': 'An error occurred while checking for existing user'}, 500

        if existing_user:
            return {'message': 'User already exists!'}, 400

        hashed_password = generate_password_hash(password)
        new_user = User(name=name, email=email, password=hashed_password)

        try:
            new_user.save()
            return {'user': new_user.to_dict()}, 201
        except Exception as e:
            api.logger.error(str(e))
            return {'message': 'An error occurred while creating the user'}, 500

@api.route('/login')
class Login(Resource):
    @api.doc('user_login')
    @api.expect(api.model('LoginCredentials', {
        'email': fields.String(required=True, description='User email'),
        'password': fields.String(required=True, description='User password'),
    }))
    @api.response(200, 'Login successful')
    @api.response(400, 'Invalid credentials')
    @api.response(404, 'User not found')
    def post(self):
        """User login"""
        data = request.json
        email, password = data.get('email'), data.get('password')

        try:
            existing_user = User.objects(email=email).first()
        except Exception as e:
            api.logger.error(str(e))
            return {'message': 'An error occurred while fetching user'}, 500

        if not existing_user:
            return {'message': 'User is not found'}, 404

        if check_password_hash(existing_user.password, password):
            return {'user': existing_user.to_dict()}, 200
        else:
            return {'message': 'Incorrect Password!'}, 400