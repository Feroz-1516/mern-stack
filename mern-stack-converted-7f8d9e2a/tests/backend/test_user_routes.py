import unittest
from unittest.mock import patch, MagicMock
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager, create_access_token

# Mock implementations
class MockUser:
    def __init__(self, id, name, email):
        self.id = id
        self.name = name
        self.email = email

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'email': self.email}

    @staticmethod
    def query():
        return MockQuery()

    def set_password(self, password):
        self.password_hash = f"hashed_{password}"

    def check_password(self, password):
        return self.password_hash == f"hashed_{password}"

class MockQuery:
    def all(self):
        return [
            MockUser(1, "User1", "user1@example.com"),
            MockUser(2, "User2", "user2@example.com")
        ]

    def filter_by(self, email):
        return MockFilterBy(email)

class MockFilterBy:
    def __init__(self, email):
        self.email = email

    def first(self):
        if self.email == "existing@example.com":
            return MockUser(3, "Existing User", "existing@example.com")
        elif self.email == "testuser@example.com":
            return MockUser(4, "Test User", "testuser@example.com")
        return None

class MockDB:
    def __init__(self):
        self.session = MagicMock()

db = MockDB()

# Create a Flask app for testing
app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'test_secret_key'
jwt = JWTManager(app)

# Import the routes
from app.routes.user_routes import user_routes
app.register_blueprint(user_routes)

class TestUserRoutes(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    @patch('app.routes.user_routes.User', MockUser)
    def test_get_all_users(self):
        response = self.client.get('/users')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('users', data)
        self.assertEqual(len(data['users']), 2)

    @patch('app.routes.user_routes.User', MockUser)
    @patch('app.routes.user_routes.db', db)
    def test_sign_up_success(self):
        data = {
            'name': 'testuser',
            'email': 'testuser@example.com',
            'password': 'password123'
        }
        response = self.client.post('/signup', json=data)
        self.assertEqual(response.status_code, 201)
        result = response.get_json()
        self.assertIn('user', result)
        self.assertEqual(result['user']['name'], 'testuser')

    @patch('app.routes.user_routes.User', MockUser)
    def test_sign_up_existing_user(self):
        data = {
            'name': 'Existing User',
            'email': 'existing@example.com',
            'password': 'password123'
        }
        response = self.client.post('/signup', json=data)
        self.assertEqual(response.status_code, 400)
        result = response.get_json()
        self.assertEqual(result['message'], 'User already exists!')

    @patch('app.routes.user_routes.User', MockUser)
    @patch('app.routes.user_routes.create_access_token')
    def test_log_in_success(self, mock_create_access_token):
        mock_create_access_token.return_value = 'mocked_jwt_token'
        data = {
            'email': 'testuser@example.com',
            'password': 'password123'
        }
        response = self.client.post('/login', json=data)
        self.assertEqual(response.status_code, 200)
        result = response.get_json()
        self.assertIn('user', result)
        self.assertIn('access_token', result)
        self.assertEqual(result['access_token'], 'mocked_jwt_token')

    @patch('app.routes.user_routes.User', MockUser)
    def test_log_in_user_not_found(self):
        data = {
            'email': 'nonexistent@example.com',
            'password': 'password123'
        }
        response = self.client.post('/login', json=data)
        self.assertEqual(response.status_code, 404)
        result = response.get_json()
        self.assertEqual(result['message'], 'User not found')

    @patch('app.routes.user_routes.User', MockUser)
    def test_log_in_incorrect_password(self):
        data = {
            'email': 'testuser@example.com',
            'password': 'wrongpassword'
        }
        response = self.client.post('/login', json=data)
        self.assertEqual(response.status_code, 400)
        result = response.get_json()
        self.assertEqual(result['message'], 'Incorrect password!')

if __name__ == '__main__':
    unittest.main()