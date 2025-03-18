from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from app.models.blog import Blog
from app.models.user import User
from app.config.db import engine
from datetime import datetime
from flasgger import swag_from

blog_controller = Blueprint('blog_controller', __name__)

@blog_controller.route('/blogs', methods=['GET'])
@swag_from({
    'responses': {
        200: {
            'description': 'List of all blogs',
            'schema': {
                'type': 'object',
                'properties': {
                    'blogs': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'id': {'type': 'integer'},
                                'title': {'type': 'string'},
                                'desc': {'type': 'string'},
                                'img': {'type': 'string'},
                                'user_id': {'type': 'integer'},
                                'date': {'type': 'string', 'format': 'date-time'}
                            }
                        }
                    }
                }
            }
        },
        404: {
            'description': 'No blogs found'
        }
    }
})
def get_all_blogs():
    with Session(engine) as session:
        blogs = session.query(Blog).all()
        if not blogs:
            return jsonify({"message": "No blogs found"}), 404
        return jsonify({"blogs": [blog.to_dict() for blog in blogs]}), 200

@blog_controller.route('/blogs', methods=['POST'])
@swag_from({
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'schema': {
                'type': 'object',
                'properties': {
                    'title': {'type': 'string'},
                    'desc': {'type': 'string'},
                    'img': {'type': 'string'},
                    'user_id': {'type': 'integer'}
                },
                'required': ['title', 'desc', 'img', 'user_id']
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Blog created successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'blog': {
                        'type': 'object',
                        'properties': {
                            'id': {'type': 'integer'},
                            'title': {'type': 'string'},
                            'desc': {'type': 'string'},
                            'img': {'type': 'string'},
                            'user_id': {'type': 'integer'},
                            'date': {'type': 'string', 'format': 'date-time'}
                        }
                    }
                }
            }
        },
        400: {
            'description': 'Unauthorized or invalid input'
        },
        500: {
            'description': 'Internal server error'
        }
    }
})
def add_blog():
    data = request.json
    title = data.get('title')
    desc = data.get('desc')
    img = data.get('img')
    user_id = data.get('user_id')

    with Session(engine) as session:
        existing_user = session.query(User).filter(User.id == user_id).first()
        if not existing_user:
            return jsonify({"message": "Unauthorized"}), 400

        new_blog = Blog(title=title, desc=desc, img=img, user_id=user_id, date=datetime.utcnow())
        session.add(new_blog)
        session.commit()
        session.refresh(new_blog)

        return jsonify({"blog": new_blog.to_dict()}), 200

@blog_controller.route('/blogs/<int:blog_id>', methods=['PUT'])
@swag_from({
    'parameters': [
        {
            'name': 'blog_id',
            'in': 'path',
            'type': 'integer',
            'required': True
        },
        {
            'name': 'body',
            'in': 'body',
            'schema': {
                'type': 'object',
                'properties': {
                    'title': {'type': 'string'},
                    'desc': {'type': 'string'}
                }
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Blog updated successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'blog': {
                        'type': 'object',
                        'properties': {
                            'id': {'type': 'integer'},
                            'title': {'type': 'string'},
                            'desc': {'type': 'string'},
                            'img': {'type': 'string'},
                            'user_id': {'type': 'integer'},
                            'date': {'type': 'string', 'format': 'date-time'}
                        }
                    }
                }
            }
        },
        404: {
            'description': 'Blog not found'
        },
        500: {
            'description': 'Unable to update'
        }
    }
})
def update_blog(blog_id):
    data = request.json
    title = data.get('title')
    desc = data.get('desc')

    with Session(engine) as session:
        blog = session.query(Blog).filter(Blog.id == blog_id).first()
        if not blog:
            return jsonify({"message": "Blog not found"}), 404

        blog.title = title
        blog.desc = desc
        session.commit()
        session.refresh(blog)

        return jsonify({"blog": blog.to_dict()}), 200

@blog_controller.route('/blogs/<int:blog_id>', methods=['GET'])
@swag_from({
    'parameters': [
        {
            'name': 'blog_id',
            'in': 'path',
            'type': 'integer',
            'required': True
        }
    ],
    'responses': {
        200: {
            'description': 'Blog details',
            'schema': {
                'type': 'object',
                'properties': {
                    'blog': {
                        'type': 'object',
                        'properties': {
                            'id': {'type': 'integer'},
                            'title': {'type': 'string'},
                            'desc': {'type': 'string'},
                            'img': {'type': 'string'},
                            'user_id': {'type': 'integer'},
                            'date': {'type': 'string', 'format': 'date-time'}
                        }
                    }
                }
            }
        },
        404: {
            'description': 'Blog not found'
        }
    }
})
def get_blog_by_id(blog_id):
    with Session(engine) as session:
        blog = session.query(Blog).filter(Blog.id == blog_id).first()
        if not blog:
            return jsonify({"message": "Blog not found"}), 404
        return jsonify({"blog": blog.to_dict()}), 200

@blog_controller.route('/blogs/<int:blog_id>', methods=['DELETE'])
@swag_from({
    'parameters': [
        {
            'name': 'blog_id',
            'in': 'path',
            'type': 'integer',
            'required': True
        }
    ],
    'responses': {
        200: {
            'description': 'Blog deleted successfully'
        },
        404: {
            'description': 'Blog not found'
        },
        500: {
            'description': 'Unable to delete'
        }
    }
})
def delete_blog(blog_id):
    with Session(engine) as session:
        blog = session.query(Blog).filter(Blog.id == blog_id).first()
        if not blog:
            return jsonify({"message": "Blog not found"}), 404

        user = session.query(User).filter(User.id == blog.user_id).first()
        if user:
            user.blogs.remove(blog)

        session.delete(blog)
        session.commit()

        return jsonify({"message": "Successfully deleted"}), 200

@blog_controller.route('/user/<int:user_id>/blogs', methods=['GET'])
@swag_from({
    'parameters': [
        {
            'name': 'user_id',
            'in': 'path',
            'type': 'integer',
            'required': True
        }
    ],
    'responses': {
        200: {
            'description': 'User blogs',
            'schema': {
                'type': 'object',
                'properties': {
                    'user': {
                        'type': 'object',
                        'properties': {
                            'id': {'type': 'integer'},
                            'name': {'type': 'string'},
                            'email': {'type': 'string'},
                            'blogs': {
                                'type': 'array',
                                'items': {
                                    'type': 'object',
                                    'properties': {
                                        'id': {'type': 'integer'},
                                        'title': {'type': 'string'},
                                        'desc': {'type': 'string'},
                                        'img': {'type': 'string'},
                                        'date': {'type': 'string', 'format': 'date-time'}
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        404: {
            'description': 'User not found'
        }
    }
})
def get_blogs_by_user_id(user_id):
    with Session(engine) as session:
        user = session.query(User).filter(User.id == user_id).first()
        if not user:
            return jsonify({"message": "User not found"}), 404

        user_data = user.to_dict()
        user_data['blogs'] = [blog.to_dict() for blog in user.blogs]
        return jsonify({"user": user_data}), 200