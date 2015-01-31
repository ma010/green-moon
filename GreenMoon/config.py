import os

basedir = os.path.abspath(os.path.dirname(__file__))
# database url
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://bear:123@localhost/blogdb'
# True: Enable automatic commits of database changes at the end of each request.
SQLALCHEMY_COMMIT_ON_TEARDOWN = True
