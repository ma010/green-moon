# -*- coding: utf-8 -*-
import os
basedir = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = 'guess'

if os.environ.get('DATABASE_URL') is None:
    SQLALCHEMY_DATABASE_URI = ('postgresql+psycopg2://nathan:789@localhost/blog.db')
else:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_RECORD_QUERIES = True

# administrator list
ADMINS = ['greenoony@gmail.com']
