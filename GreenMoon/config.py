'''
This script configures the database
'''

# -*- coding: utf-8 -*-
import os

# This will make adjustment of database URL more flexible in the future
if os.environ.get('DATABASE_URL') is None:
    SQLALCHEMY_DATABASE_URI = ('postgresql+psycopg2://PATH:PASSWORD@localhost/DATABASENAME')
else:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

# True: Enable automatic commits of database changes at the end of each request
SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    
# a repository for database migration 
#SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')


