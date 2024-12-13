from flask import Blueprint
from flask_restx import Api, Resource
from .user_controller import get_all_users, sign_up, log_in

user_routes = Blueprint('user_routes', __name__)
api = Api(user_routes, doc='/doc/')

@api.route('/')
class UserList(Resource):
    @api.doc(description='Get all users')
    def get(self):
        """Get all users"""
        return get_all_users()

@api.route('/signup')
class UserSignUp(Resource):
    @api.doc(description='Sign up a new user')
    def post(self):
        """Sign up a new user"""
        return sign_up()

@api.route('/login')
class UserLogin(Resource):
    @api.doc(description='Log in a user')
    def post(self):
        """Log in a user"""
        return log_in()