from GreenMoon import app
from GreenMoon.db_init import dbSQL#, dbMongo
from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

class Account(dbSQL.Model):
    __tablename__ = 'accounts'
    name = dbSQL.Column(dbSQL.String(12), primary_key=True, unique=True)
    password_hash = dbSQL.Column(dbSQL.String(128))

    @property
    def password(self):
        raise AttributeError('Password cannot be read directly!')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<Account name %r>' % self.name

# block below is temporarily abandoned
'''
# define a User table to store user id, nickname, email and posts
class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    postTitle = db.Column(db.String(2000), index=True, unique=True)
    postBody = db.Column(db.String(2000), index=True, unique=True)

    def __repr__(self):
        return '<User %r>' % (self.nickname)


# define a class Post -- a second table in the database
# to store User's Post separately


## Needs more input from Bo
# Define a method to draw data from MongoDB and then print
def allTupleFromDB():
    output = ""
    allLicense = dbMongo.activeLicense.find()
    for L in allLicense:
        output += str(L['zip']) + '++'
        temp = ' '.join( str(e) for e in list( L['license'].keys() ) )
        output += temp + '++\t\n'+'++++++++\n'
    return output
'''
