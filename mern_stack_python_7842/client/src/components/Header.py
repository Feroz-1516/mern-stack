from flask import Flask, render_template, request, redirect, url_for
from flask_login import current_user, login_required
from flask_wtf import FlaskForm
from wtforms import SubmitField
from wtforms.validators import DataRequired
from werkzeug.utils import redirect
from flask_material import Material

from .store import auth_actions, set_darkmode
from .utils.theme import lightTheme, darkTheme

app = Flask(__name__)
Material(app)

class HeaderForm(FlaskForm):
    logout = SubmitField('Logout')
    toggle_darkmode = SubmitField('Toggle Dark Mode')

@app.route('/')
def header():
    form = HeaderForm()
    is_dark = app.config.get('IS_DARK', False)
    theme = darkTheme if is_dark else lightTheme
    is_logged_in = current_user.is_authenticated

    if form.validate_on_submit():
        if form.logout.data:
            auth_actions.logout()
            return redirect(url_for('login'))
        elif form.toggle_darkmode.data:
            app.config['IS_DARK'] = not is_dark
            set_darkmode(not is_dark)

    return render_template('header.html', form=form, is_logged_in=is_logged_in, theme=theme)

@app.route('/blogs')
@login_required
def all_blogs():
    return render_template('blogs.html')

@app.route('/myBlogs')
@login_required
def my_blogs():
    return render_template('my_blogs.html')

@app.route('/blogs/add')
@login_required
def add_blog():
    return render_template('add_blog.html')

if __name__ == '__main__':
    app.run(debug=True)