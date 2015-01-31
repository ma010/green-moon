from flask import render_template
from GreenMoon import app

@app.route('/')
@app.route('/index')
def index():
    return 'Hello, world!'

