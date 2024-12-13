from flask import request, jsonify
from flask_restx import Resource, Api, fields
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv

load_dotenv()

api = Api()

# Import the necessary components from a UI library (e.g., Flask-WTF for forms)
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

# Import the config file
import sys
sys.path.append('..')
from config import BASE_URL

class BlogForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')

blog_model = api.model('Blog', {
    'title': fields.String(required=True, description='Blog title'),
    'description': fields.String(required=True, description='Blog description')
})

@api.route('/api/blogs/<string:id>')
class BlogDetail(Resource):
    @api.doc(params={'id': 'Blog ID'})
    def get(self, id):
        try:
            response = requests.get(f"{BASE_URL}/api/blogs/{id}")
            response.raise_for_status()
            data = response.json()
            return jsonify(data)
        except requests.RequestException as e:
            api.abort(500, f"Error fetching blog details: {str(e)}")

    @api.doc(params={'id': 'Blog ID'})
    @api.expect(blog_model)
    def put(self, id):
        try:
            data = api.payload
            response = requests.put(f"{BASE_URL}/api/blogs/update/{id}", json=data)
            response.raise_for_status()
            return jsonify(response.json())
        except requests.RequestException as e:
            api.abort(500, f"Error updating blog: {str(e)}")

# This part would typically be in your main Flask application file
from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)
CORS(app)
api.init_app(app)

@app.route('/blog/<string:id>', methods=['GET', 'POST'])
def blog_detail(id):
    form = BlogForm()
    if form.validate_on_submit():
        data = {
            'title': form.title.data,
            'description': form.description.data
        }
        response = requests.put(f"{BASE_URL}/api/blogs/update/{id}", json=data)
        if response.ok:
            return redirect(url_for('user_blogs'))
    
    response = requests.get(f"{BASE_URL}/api/blogs/{id}")
    if response.ok:
        blog_data = response.json()['blog']
        form.title.data = blog_data['title']
        form.description.data = blog_data['description']
    
    return render_template('blog_detail.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)