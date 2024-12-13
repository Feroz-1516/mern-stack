from flask import Flask
from flask_restx import Api, Resource, fields
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from pymongo import MongoClient
import os
from dotenv import load_load_dotenv

load_dotenv()

app = Flask(__name__)
api = Api(app, version='1.0', title='Blog API', description='A simple blog API')
jwt = JWTManager(app)
CORS(app)

# MongoDB connection
client = MongoClient(os.getenv('MONGODB_URI'))
db = client[os.getenv('DB_NAME')]

# Models
auth_model = api.model('Auth', {
    'is_logged_in': fields.Boolean(required=True, description='Login status')
})

theme_model = api.model('Theme', {
    'is_darkmode': fields.Boolean(required=True, description='Dark mode status')
})

# Namespaces
auth_ns = api.namespace('auth', description='Authentication operations')
theme_ns = api.namespace('theme', description='Theme operations')

@auth_ns.route('/')
class Auth(Resource):
    @api.marshal_with(auth_model)
    def get(self):
        return {'is_logged_in': False}

    @api.expect(auth_model)
    @api.marshal_with(auth_model)
    def post(self):
        data = api.payload
        if data['is_logged_in']:
            print("Updating login status")
        return data

    @api.marshal_with(auth_model)
    def delete(self):
        # Remove userId from session or token
        return {'is_logged_in': False}

@theme_ns.route('/')
class Theme(Resource):
    @api.marshal_with(theme_model)
    def get(self):
        return {'is_darkmode': False}

    @api.expect(theme_model)
    @api.marshal_with(theme_model)
    def post(self):
        return api.payload

if __name__ == '__main__':
    app.run(debug=True)