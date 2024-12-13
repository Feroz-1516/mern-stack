import React from 'react'
from flask import Flask, jsonify, request
import requests
from components.Blogs import Blogs
from components.DeleteBlogs import DeleteButton
from config import BASE_URL

app = Flask(__name__)

class UserBlogs(React.Component):
    def __init__(self):
        super().__init__()
        self.state = {
            'user': None
        }
        self.id = self.get_user_id()

    def get_user_id(self):
        # In a real Flask app, you'd use Flask-Login or similar for session management
        # This is a placeholder to mimic localStorage.getItem("userId")
        return request.cookies.get('userId')

    def send_request(self):
        try:
            response = requests.get(f"{BASE_URL}/api/blogs/user/{self.id}")
            response.raise_for_status()
            data = response.json()
            return data
        except requests.RequestException as e:
            print(f"Error: {e}")
            return None

    def component_did_mount(self):
        data = self.send_request()
        if data:
            self.setState({'user': data['user']})

    def handle_delete(self, blog_id):
        try:
            response = requests.delete(f"{BASE_URL}/api/blogs/{blog_id}")
            response.raise_for_status()
            data = self.send_request()
            if data:
                self.setState({'user': data['user']})
        except requests.RequestException as e:
            print(f"Error deleting blog: {e}")

    def render(self):
        user = self.state['user']
        if user and user['blogs']:
            return (
                <div className="container">
                    {user['blogs'].map((blog, index) => (
                        <div key={index} className="blog-container">
                            <Blogs
                                id={blog['_id']}
                                isUser={True}
                                title={blog['title']}
                                description={blog['description']}
                                imageURL={blog['image']}
                                userName={user['name']}
                            />
                            <img
                                className="blog-image"
                                src={blog['image']}
                                alt={blog['title']}
                            />
                            <DeleteButton blogId={blog['_id']} onDelete={self.handle_delete} />
                        </div>
                    ))}
                </div>
            )
        return None

@app.route('/api/user-blogs')
def user_blogs():
    user_blogs = UserBlogs()
    user_blogs.component_did_mount()
    return jsonify(user_blogs.state)

if __name__ == '__main__':
    app.run(debug=True)