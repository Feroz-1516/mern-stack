from flask import Flask, jsonify, request
from flask_cors import CORS
from flasgger import Swagger
from app.routes.user_routes import user_routes
from app.routes.blog_routes import blog_routes
from app.config.db import init_db

app = Flask(__name__)
CORS(app)

# Configure Swagger
swagger = Swagger(app)

# Initialize database
init_db()

# Register blueprints
app.register_blueprint(user_routes, url_prefix='/api/users')
app.register_blueprint(blog_routes, url_prefix='/api/blogs')

@app.route('/api', methods=['GET'])
def hello():
    """
    A simple hello world endpoint
    ---
    responses:
      200:
        description: A greeting message
    """
    return jsonify({"message": "hello"})

if __name__ == "__main__":
    app.run(port=5001, debug=True)