import pytest
from flask import json
from server.server import app
from server.controller.user_controller import UserList, SignUp, Login
from server.model.user import User
from bson import ObjectId

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get_all_users(client):
    response = client.get('/api/users')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)

def test_signup(client):
    new_user = {
        'name': 'Test User',
        'email': 'testuser@example.com',
        'password': 'testpassword'
    }
    response = client.post('/api/users/signup', json=new_user)
    assert response.status_code == 201
    data = json.loads(response.data)
    assert 'id' in data
    assert data['name'] == new_user['name']
    assert data['email'] == new_user['email']

    # Clean up: Delete the created user
    User.objects(email=new_user['email']).delete()

def test_login(client):
    # First, create a user
    user = User(name='Login Test User', email='logintest@example.com', password='testpassword').save()

    login_data = {
        'email': 'logintest@example.com',
        'password': 'testpassword'
    }
    response = client.post('/api/users/login', json=login_data)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'id' in data
    assert data['email'] == login_data['email']

    # Clean up: Delete the created user
    user.delete()

def test_login_invalid_credentials(client):
    login_data = {
        'email': 'nonexistent@example.com',
        'password': 'wrongpassword'
    }
    response = client.post('/api/users/login', json=login_data)
    assert response.status_code == 401
    data = json.loads(response.data)
    assert 'message' in data
    assert data['message'] == 'Invalid email or password'

def test_signup_duplicate_email(client):
    # First, create a user
    existing_user = User(name='Existing User', email='existing@example.com', password='testpassword').save()

    new_user = {
        'name': 'Duplicate User',
        'email': 'existing@example.com',
        'password': 'newpassword'
    }
    response = client.post('/api/users/signup', json=new_user)
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'message' in data
    assert 'already exists' in data['message']

    # Clean up: Delete the created user
    existing_user.delete()