import pytest
from flask import json
from server.server import app
from server.controller.blog_controller import BlogList, BlogItem, UserBlogs
from server.model.blog import Blog
from server.model.user import User
from bson import ObjectId

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get_all_blogs(client, mocker):
    # Mock the Blog.objects.all() method
    mock_blogs = [
        Blog(title="Test Blog 1", desc="Description 1", img="image1.jpg", user=ObjectId()),
        Blog(title="Test Blog 2", desc="Description 2", img="image2.jpg", user=ObjectId())
    ]
    mocker.patch('server.model.blog.Blog.objects.all', return_value=mock_blogs)

    response = client.get('/api/blogs')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 2
    assert data[0]['title'] == "Test Blog 1"
    assert data[1]['title'] == "Test Blog 2"

def test_create_blog(client, mocker):
    # Mock the User.objects.get() method
    mock_user = User(id=ObjectId(), name="Test User", email="test@example.com")
    mocker.patch('server.model.user.User.objects.get', return_value=mock_user)

    # Mock the Blog.save() method
    mocker.patch('server.model.blog.Blog.save')

    blog_data = {
        "title": "New Test Blog",
        "desc": "New Description",
        "img": "new_image.jpg",
        "user": str(mock_user.id)
    }

    response = client.post('/api/blogs', json=blog_data)
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['title'] == "New Test Blog"
    assert data['desc'] == "New Description"

def test_get_blog_by_id(client, mocker):
    mock_blog = Blog(id=ObjectId(), title="Test Blog", desc="Description", img="image.jpg", user=ObjectId())
    mocker.patch('server.model.blog.Blog.objects.get', return_value=mock_blog)

    response = client.get(f'/api/blogs/{str(mock_blog.id)}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['title'] == "Test Blog"
    assert data['desc'] == "Description"

def test_update_blog(client, mocker):
    mock_blog = Blog(id=ObjectId(), title="Old Title", desc="Old Description", img="old_image.jpg", user=ObjectId())
    mocker.patch('server.model.blog.Blog.objects.get', return_value=mock_blog)
    mocker.patch('server.model.blog.Blog.save')

    update_data = {
        "title": "Updated Title",
        "desc": "Updated Description",
        "img": "updated_image.jpg"
    }

    response = client.put(f'/api/blogs/{str(mock_blog.id)}', json=update_data)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['title'] == "Updated Title"
    assert data['desc'] == "Updated Description"

def test_delete_blog(client, mocker):
    mock_blog = Blog(id=ObjectId(), title="Test Blog", desc="Description", img="image.jpg", user=ObjectId())
    mocker.patch('server.model.blog.Blog.objects.get', return_value=mock_blog)
    mocker.patch('server.model.blog.Blog.delete')

    response = client.delete(f'/api/blogs/{str(mock_blog.id)}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['message'] == "Blog deleted successfully"

def test_get_user_blogs(client, mocker):
    mock_user = User(id=ObjectId(), name="Test User", email="test@example.com")
    mock_blogs = [
        Blog(title="User Blog 1", desc="Description 1", img="image1.jpg", user=mock_user.id),
        Blog(title="User Blog 2", desc="Description 2", img="image2.jpg", user=mock_user.id)
    ]
    mocker.patch('server.model.user.User.objects.get', return_value=mock_user)
    mocker.patch('server.model.blog.Blog.objects', return_value=mock_blogs)

    response = client.get(f'/api/blogs/user/{str(mock_user.id)}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 2
    assert data[0]['title'] == "User Blog 1"
    assert data[1]['title'] == "User Blog 2"