"""
    This script initializes the web app
"""


from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from pymongo import Connection

app = Flask(__name__)
dbSQL = SQLAlchemy(app)

# SQL DB for core/structured storage, such as  by organizing or parsing data from MongoDB
# Set up connection with postgresql
app.config.from_pyfile('config.py')

# MongoDB for fast unstructured data storage, such as info crawled from webpages, twitter, etc.
# Set up mongoDB engine
con = Connection()
# Get database record - businessDB which contains business lincense info
dbMongo = con.businessDB

from GreenMoon import views

