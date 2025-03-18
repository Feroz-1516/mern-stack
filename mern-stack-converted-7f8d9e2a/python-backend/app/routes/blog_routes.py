from flask import Blueprint, request, jsonify
from app.controllers.blog_controller import (
    get_all_blogs,
    add_blog,
    update_blog,
    get_blog_by_id,
    delete_blog,
    get_blogs_by_user_id
)
from flasgger import swag_from

blog_routes = Blueprint('blog_routes', __name__)

@blog_routes.route('/', methods=['GET'])
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
        }
    }
})
def get_blogs():
    return get_all_blogs()

@blog_routes.route('/add', methods=['POST'])
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
            'description': 'Blog added successfully',
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
        }
    }
})
def create_blog():
    return add_blog()

@blog_routes.route('/update/<int:id>', methods=['PUT'])
@swag_from({
    'parameters': [
        {
            'name': 'id',
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
        }
    }
})
def modify_blog(id):
    return update_blog(id)

@blog_routes.route('/<int:id>', methods=['GET'])
@swag_from({
    'parameters': [
        {
            'name': 'id',
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
        }
    }
})
def get_blog(id):
    return get_blog_by_id(id)

@blog_routes.route('/<int:id>', methods=['DELETE'])
@swag_from({
    'parameters': [
        {
            'name': 'id',
            'in': 'path',
            'type': 'integer',
            'required': True
        }
    ],
    'responses': {
        200: {
            'description': 'Blog deleted successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string'}
                }
            }
        }
    }
})
def remove_blog(id):
    return delete_blog(id)

@blog_routes.route('/user/<int:id>', methods=['GET'])
@swag_from({
    'parameters': [
        {
            'name': 'id',
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
        }
    }
})
def get_user_blogs(id):
    return get_blogs_by_user_id(id)