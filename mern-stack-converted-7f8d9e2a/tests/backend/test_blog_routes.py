import unittest
from unittest.mock import patch, MagicMock
from flask import Flask, json
from app.routes.blog_routes import blog_routes

class TestBlogRoutes(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(blog_routes)
        self.client = self.app.test_client()

    def test_get_all_blogs(self):
        mock_blogs = [
            {'id': 1, 'title': 'Sample Blog 1', 'content': 'This is the content of sample blog 1'},
            {'id': 2, 'title': 'Sample Blog 2', 'content': 'This is the content of sample blog 2'}
        ]
        
        with patch('app.routes.blog_routes.get_all_blogs') as mock_get_all_blogs:
            mock_get_all_blogs.return_value = json.dumps({'blogs': mock_blogs}), 200
            
            response = self.client.get('/')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(json.loads(response.data), {'blogs': mock_blogs})

    def test_add_blog(self):
        new_blog = {
            'title': 'New Blog',
            'desc': 'This is a new blog post',
            'img': 'image_url',
            'user_id': 1
        }
        expected_response = {
            'blog': {
                'id': 3,
                'title': 'New Blog',
                'desc': 'This is a new blog post',
                'img': 'image_url',
                'user_id': 1,
                'date': '2023-05-20T10:00:00Z'
            }
        }
        
        with patch('app.routes.blog_routes.add_blog') as mock_add_blog:
            mock_add_blog.return_value = json.dumps(expected_response), 200
            
            response = self.client.post('/add', json=new_blog)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(json.loads(response.data), expected_response)

    def test_update_blog(self):
        update_data = {
            'title': 'Updated Blog Title',
            'desc': 'This is the updated content'
        }
        expected_response = {
            'blog': {
                'id': 1,
                'title': 'Updated Blog Title',
                'desc': 'This is the updated content',
                'img': 'image_url',
                'user_id': 1,
                'date': '2023-05-20T11:00:00Z'
            }
        }
        
        with patch('app.routes.blog_routes.update_blog') as mock_update_blog:
            mock_update_blog.return_value = json.dumps(expected_response), 200
            
            response = self.client.put('/update/1', json=update_data)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(json.loads(response.data), expected_response)

    def test_get_blog_by_id(self):
        expected_blog = {
            'blog': {
                'id': 1,
                'title': 'Sample Blog 1',
                'desc': 'This is the content of sample blog 1',
                'img': 'image_url',
                'user_id': 1,
                'date': '2023-05-20T09:00:00Z'
            }
        }
        
        with patch('app.routes.blog_routes.get_blog_by_id') as mock_get_blog_by_id:
            mock_get_blog_by_id.return_value = json.dumps(expected_blog), 200
            
            response = self.client.get('/1')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(json.loads(response.data), expected_blog)

    def test_delete_blog(self):
        expected_response = {'message': 'Blog deleted successfully'}
        
        with patch('app.routes.blog_routes.delete_blog') as mock_delete_blog:
            mock_delete_blog.return_value = json.dumps(expected_response), 200
            
            response = self.client.delete('/1')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(json.loads(response.data), expected_response)

    def test_get_blogs_by_user_id(self):
        expected_response = {
            'user': {
                'id': 1,
                'name': 'John Doe',
                'email': 'john@example.com',
                'blogs': [
                    {
                        'id': 1,
                        'title': 'Sample Blog 1',
                        'desc': 'This is the content of sample blog 1',
                        'img': 'image_url',
                        'date': '2023-05-20T09:00:00Z'
                    },
                    {
                        'id': 3,
                        'title': 'New Blog',
                        'desc': 'This is a new blog post',
                        'img': 'image_url',
                        'date': '2023-05-20T10:00:00Z'
                    }
                ]
            }
        }
        
        with patch('app.routes.blog_routes.get_blogs_by_user_id') as mock_get_blogs_by_user_id:
            mock_get_blogs_by_user_id.return_value = json.dumps(expected_response), 200
            
            response = self.client.get('/user/1')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(json.loads(response.data), expected_response)

    def test_get_all_blogs_error(self):
        with patch('app.routes.blog_routes.get_all_blogs') as mock_get_all_blogs:
            mock_get_all_blogs.side_effect = Exception("Database error")
            
            response = self.client.get('/')
            self.assertEqual(response.status_code, 500)
            self.assertIn("An error occurred", json.loads(response.data)['message'])

    def test_add_blog_invalid_data(self):
        invalid_blog = {
            'title': 'New Blog',
            # Missing required fields
        }
        
        response = self.client.post('/add', json=invalid_blog)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid input", json.loads(response.data)['message'])

    def test_update_blog_not_found(self):
        update_data = {
            'title': 'Updated Blog Title',
            'desc': 'This is the updated content'
        }
        
        with patch('app.routes.blog_routes.update_blog') as mock_update_blog:
            mock_update_blog.return_value = json.dumps({'message': 'Blog not found'}), 404
            
            response = self.client.put('/update/999', json=update_data)
            self.assertEqual(response.status_code, 404)
            self.assertEqual(json.loads(response.data), {'message': 'Blog not found'})

    def test_get_blog_by_id_not_found(self):
        with patch('app.routes.blog_routes.get_blog_by_id') as mock_get_blog_by_id:
            mock_get_blog_by_id.return_value = json.dumps({'message': 'Blog not found'}), 404
            
            response = self.client.get('/999')
            self.assertEqual(response.status_code, 404)
            self.assertEqual(json.loads(response.data), {'message': 'Blog not found'})

    def test_delete_blog_not_found(self):
        with patch('app.routes.blog_routes.delete_blog') as mock_delete_blog:
            mock_delete_blog.return_value = json.dumps({'message': 'Blog not found'}), 404
            
            response = self.client.delete('/999')
            self.assertEqual(response.status_code, 404)
            self.assertEqual(json.loads(response.data), {'message': 'Blog not found'})

    def test_get_blogs_by_user_id_not_found(self):
        with patch('app.routes.blog_routes.get_blogs_by_user_id') as mock_get_blogs_by_user_id:
            mock_get_blogs_by_user_id.return_value = json.dumps({'message': 'User not found'}), 404
            
            response = self.client.get('/user/999')
            self.assertEqual(response.status_code, 404)
            self.assertEqual(json.loads(response.data), {'message': 'User not found'})

if __name__ == '__main__':
    unittest.main()