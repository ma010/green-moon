import os

# Use the following commands to create an account on the database server:
#   CREATE USER 'greenmoon'@'localhost' IDENTIFIED BY 'greenmoon';
#   GRANT ALL PRIVILEGES ON *.* TO 'greenmoon'@'localhost' WITH GRANT OPTION;
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://greenmoon:greenmoon@localhost/bbsdb'
# True: Enable automatic commits of database changes at the end of each request.
SQLALCHEMY_COMMIT_ON_TEARDOWN = True
