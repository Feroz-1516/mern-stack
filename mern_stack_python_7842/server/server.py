from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
from routes.user_routes import user_routes
from routes.blog_routes import blog_routes
from config.db import init_db

app = Flask(__name__)
CORS(app)

# Initialize database
init_db()

# Swagger configuration
SWAGGER_URL = '/api/docs'
API_URL = '/static/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Blog API"
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# Register routes
app.register_blueprint(user_routes, url_prefix='/api/users')
app.register_blueprint(blog_routes, url_prefix='/api/blogs')

@app.route('/api', methods=['GET'])
def hello():
    """
    A simple hello endpoint
    ---
    responses:
      200:
        description: A simple greeting message
    """
    return jsonify({"message": "hello"})

if __name__ == '__main__':
    app.run(port=5001, debug=True)