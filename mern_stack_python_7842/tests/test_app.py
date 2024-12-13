import pytest
from flask import url_for
from server.server import app
from server.model.user import User
from server.model.blog import Blog

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index_route(client):
    response = client.get('/api')
    assert response.status_code == 200
    assert b"hello" in response.data

def test_get_all_users(client):
    response = client.get('/api/users')
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_signup_user(client):
    user_data = {
        "name": "Test User",
        "email": "testuser@example.com",
        "password": "testpassword"
    }
    response = client.post('/api/users/signup', json=user_data)
    assert response.status_code == 201
    assert "user" in response.json
    assert "token" in response.json

def test_login_user(client):
    login_data = {
        "email": "testuser@example.com",
        "password": "testpassword"
    }
    response = client.post('/api/users/login', json=login_data)
    assert response.status_code == 200
    assert "user" in response.json
    assert "token" in response.json

def test_get_all_blogs(client):
    response = client.get('/api/blogs')
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_create_blog(client):
    # First, login to get a token
    login_data = {
        "email": "testuser@example.com",
        "password": "testpassword"
    }
    login_response = client.post('/api/users/login', json=login_data)
    token = login_response.json['token']

    blog_data = {
        "title": "Test Blog",
        "desc": "This is a test blog post",
        "img": "https://example.com/test.jpg"
    }
    headers = {'Authorization': f'Bearer {token}'}
    response = client.post('/api/blogs', json=blog_data, headers=headers)
    assert response.status_code == 201
    assert "blog" in response.json

def test_get_blog_by_id(client):
    # Assuming a blog exists with id 1
    response = client.get('/api/blogs/1')
    assert response.status_code == 200
    assert "blog" in response.json

def test_update_blog(client):
    # First, login to get a token
    login_data = {
        "email": "testuser@example.com",
        "password": "testpassword"
    }
    login_response = client.post('/api/users/login', json=login_data)
    token = login_response.json['token']

    # Assuming a blog exists with id 1
    blog_data = {
        "title": "Updated Test Blog",
        "desc": "This is an updated test blog post",
        "img": "https://example.com/updated.jpg"
    }
    headers = {'Authorization': f'Bearer {token}'}
    response = client.put('/api/blogs/1', json=blog_data, headers=headers)
    assert response.status_code == 200
    assert "blog" in response.json

def test_delete_blog(client):
    # First, login to get a token
    login_data = {
        "email": "testuser@example.com",
        "password": "testpassword"
    }
    login_response = client.post('/api/users/login', json=login_data)
    token = login_response.json['token']

    # Assuming a blog exists with id 1
    headers = {'Authorization': f'Bearer {token}'}
    response = client.delete('/api/blogs/1', headers=headers)
    assert response.status_code == 200
    assert "message" in response.json

def test_get_user_blogs(client):
    # Assuming a user exists with id 1
    response = client.get('/api/blogs/user/1')
    assert response.status_code == 200
    assert isinstance(response.json, list)