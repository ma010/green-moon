from flask import Flask
#from pymongo import Connection

app = Flask(__name__)
app.config.from_pyfile('config.py')

from GreenMoon import views
