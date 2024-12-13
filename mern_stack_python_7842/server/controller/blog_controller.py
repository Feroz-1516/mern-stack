from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from bson import ObjectId
from models.blog import Blog
from models.user import User

api = Namespace('blogs', description='Blog operations')

blog_model = api.model('Blog', {
    'title': fields.String(required=True, description='The blog title'),
    'desc': fields.String(required=True, description='The blog description'),
    'img': fields.String(required=True, description='The blog image URL'),
    'user': fields.String(required=True, description='The user ID')
})

@api.route('/')
class BlogList(Resource):
    @api.doc('list_blogs')
    @api.response(200, 'Success')
    @api.response(404, 'No blogs found')
    def get(self):
        """List all blogs"""
        try:
            blogs = Blog.objects.all()
            if not blogs:
                return {'message': 'No blogs found'}, 404
            return jsonify([blog.to_dict() for blog in blogs])
        except Exception as e:
            api.logger.error(str(e))
            return {'message': 'An error occurred'}, 500

    @api.doc('create_blog')
    @api.expect(blog_model)
    @api.response(201, 'Blog created successfully')
    @api.response(400, 'Invalid user')
    @api.response(500, 'Server error')
    def post(self):
        """Create a new blog"""
        data = request.json
        user_id = data.get('user')

        try:
            existing_user = User.objects.get(id=ObjectId(user_id))
        except User.DoesNotExist:
            return {'message': 'Unauthorized'}, 400

        blog = Blog(
            title=data['title'],
            desc=data['desc'],
            img=data['img'],
            user=existing_user,
            date=datetime.utcnow()
        )

        try:
            blog.save()
            existing_user.blogs.append(blog)
            existing_user.save()
            return blog.to_dict(), 201
        except Exception as e:
            api.logger.error(str(e))
            return {'message': str(e)}, 500

@api.route('/<string:id>')
@api.param('id', 'The blog identifier')
class BlogItem(Resource):
    @api.doc('get_blog')
    @api.response(200, 'Success')
    @api.response(404, 'Blog not found')
    def get(self, id):
        """Fetch a blog given its identifier"""
        try:
            blog = Blog.objects.get(id=ObjectId(id))
            return blog.to_dict()
        except Blog.DoesNotExist:
            api.abort(404, message='Blog not found')

    @api.doc('update_blog')
    @api.expect(blog_model)
    @api.response(200, 'Blog updated successfully')
    @api.response(404, 'Blog not found')
    @api.response(500, 'Unable to update')
    def put(self, id):
        """Update a blog given its identifier"""
        data = request.json
        try:
            blog = Blog.objects.get(id=ObjectId(id))
            blog.update(title=data['title'], desc=data['desc'])
            return blog.to_dict()
        except Blog.DoesNotExist:
            api.abort(404, message='Blog not found')
        except Exception as e:
            api.logger.error(str(e))
            return {'message': 'Unable to update'}, 500

    @api.doc('delete_blog')
    @api.response(200, 'Blog deleted successfully')
    @api.response(404, 'Blog not found')
    @api.response(500, 'Unable to delete')
    def delete(self, id):
        """Delete a blog given its identifier"""
        try:
            blog = Blog.objects.get(id=ObjectId(id))
            user = blog.user
            user.blogs.remove(blog)
            user.save()
            blog.delete()
            return {'message': 'Successfully deleted'}
        except Blog.DoesNotExist:
            api.abort(404, message='Blog not found')
        except Exception as e:
            api.logger.error(str(e))
            return {'message': 'Unable to delete'}, 500

@api.route('/user/<string:id>')
@api.param('id', 'The user identifier')
class UserBlogs(Resource):
    @api.doc('get_user_blogs')
    @api.response(200, 'Success')
    @api.response(404, 'User not found')
    def get(self, id):
        """Fetch all blogs for a given user"""
        try:
            user = User.objects.get(id=ObjectId(id))
            return {'user': user.to_dict(include_blogs=True)}
        except User.DoesNotExist:
            api.abort(404, message='User not found')