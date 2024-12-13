from flask import Blueprint, request
from flask_restx import Api, Resource
from server.controller.blog_controller import (
    get_all_blogs, add_blog, update_blog, get_by_id, delete_blog, get_by_user_id
)

blog_routes = Blueprint('blog_routes', __name__)
api = Api(blog_routes, doc='/api/docs', title='Blog API', description='API for managing blogs')

@api.route('/blogs')
class BlogList(Resource):
    @api.doc(description='Get all blogs')
    def get(self):
        return get_all_blogs()

    @api.doc(description='Add a new blog')
    def post(self):
        return add_blog()

@api.route('/blogs/<string:id>')
class BlogItem(Resource):
    @api.doc(description='Get a blog by ID')
    def get(self, id):
        return get_by_id(id)

    @api.doc(description='Update a blog')
    def put(self, id):
        return update_blog(id)

    @api.doc(description='Delete a blog')
    def delete(self, id):
        return delete_blog(id)

@api.route('/blogs/user/<string:id>')
class UserBlogs(Resource):
    @api.doc(description='Get blogs by user ID')
    def get(self, id):
        return get_by_user_id(id)