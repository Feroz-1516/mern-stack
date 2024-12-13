from flask import Flask, render_template
from flask_cors import CORS
from flask_restful import Api
from components.Header import Header
from components.Login import Login
from components.Blogs import Blogs
from components.UserBlogs import UserBlogs
from components.AddBlogs import AddBlogs
from components.BlogDetail import BlogDetail

app = Flask(__name__)
CORS(app)
api = Api(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return Login().render()

@app.route('/blogs')
def blogs():
    return Blogs().render()

@app.route('/myBlogs')
def user_blogs():
    return UserBlogs().render()

@app.route('/myBlogs/<int:id>')
def blog_detail(id):
    return BlogDetail(id).render()

@app.route('/blogs/add')
def add_blogs():
    return AddBlogs().render()

if __name__ == '__main__':
    app.run(debug=True)