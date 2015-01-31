import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from .config import basedir
from pymongo import Connection

app = Flask(__name__)

# set up db connection with mongoDB
con = Connection()
db = con.businessDB

# set up dbSQL connection with postgresql
app.config.from_pyfile('config.py')
dbSQL = SQLAlchemy(app)

from GreenMoon import views
