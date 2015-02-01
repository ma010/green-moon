# -*- coding: utf-8 -*-
import os

# This will make adjustment of URI more flexible in the future
if os.environ.get('DATABASE_URL') is None:
    SQLALCHEMY_DATABASE_URI = ('postgresql+psycopg2://greenmoon:greenmoon@localhost/blog.db')
else:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

# a repository for database migration 
#SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

# Unknown feature; check back later
#SQLALCHEMY_RECORD_QUERIES = True

# administrator list

