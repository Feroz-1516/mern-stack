from flask import Flask, render_template
from flask_cors import CORS
from flask_redux import Redux
from flask_router import Router
from app import App
from store import store

app = Flask(__name__)
CORS(app)
redux = Redux(app)
router = Router(app)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    redux.init_app(store)
    router.init_app()
    app.run(debug=True)

# If you want to start measuring performance in your app, pass a function
# to log results (for example: from flask_web_vitals import report_web_vitals)
# or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals