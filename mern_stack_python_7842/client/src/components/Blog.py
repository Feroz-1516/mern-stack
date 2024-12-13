from flask import render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired
from werkzeug.utils import secure_filename
import os
from config import Config
from utils import create_styles

class BlogForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    image = StringField('Image URL', validators=[DataRequired()])
    submit = SubmitField('Submit')

def blog_view(title, desc, img, user, is_user, id):
    classes = create_styles()
    
    form = BlogForm()
    
    if form.validate_on_submit():
        if form.submit.data:
            # Handle form submission (edit or delete)
            if is_user:
                if 'edit' in request.form:
                    return redirect(url_for('my_blogs', id=id))
                elif 'delete' in request.form:
                    # Implement delete functionality
                    delete_blog(id)
                    return redirect(url_for('index'))
    
    return render_template('blog.html', 
                           title=title, 
                           desc=desc, 
                           img=img, 
                           user=user, 
                           is_user=is_user, 
                           id=id, 
                           form=form, 
                           classes=classes)

def delete_blog(blog_id):
    # Implement the delete functionality here
    # This should make an API call to delete the blog
    pass