# -*- coding: utf-8 -*-
import os

# This will make adjustment of URI more flexible in the future
if os.environ.get('DATABASE_URL') is None:
    SQLALCHEMY_DATABASE_URI = ('postgresql+psycopg2://greenmoon:greenmoon@localhost/blogdb')
else:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

# True: Enable automatic commits of database changes at the end of each request.
SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    
# a repository for database migration 
#SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

# Unknown feature; check back later
#SQLALCHEMY_RECORD_QUERIES = True

# administrator list

