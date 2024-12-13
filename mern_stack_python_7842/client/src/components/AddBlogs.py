from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired
import requests
import json
from config import BASE_URL

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with a real secret key

class AddBlogForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    imageURL = StringField('ImageURL', validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route('/add_blog', methods=['GET', 'POST'])
def add_blog():
    form = AddBlogForm()
    if form.validate_on_submit():
        blog_data = {
            'title': form.title.data,
            'desc': form.description.data,
            'img': form.imageURL.data,
            'user': request.cookies.get('userId')  # Assuming userId is stored in a cookie
        }
        response = requests.post(f"{BASE_URL}/api/blogs/add", json=blog_data)
        if response.status_code == 200:
            print(response.json())
            return redirect(url_for('blogs'))
        else:
            print(f"Error: {response.status_code}")
    return render_template('add_blog.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)