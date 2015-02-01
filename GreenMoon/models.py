from GreenMoon import app, dbMongo
from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import re

app.secret_key = 'why would I tell you my secret key?'

## Initialize dbSQL and and admin
dbSQL = SQLAlchemy(app)

class Account(dbSQL.Model):
    __tablename__ = 'accounts'
    id = dbSQL.Column(dbSQL.Integer, primary_key=True)
    nickname = dbSQL.Column(dbSQL.String(12), index=True, unique=True)
    password_hash = dbSQL.Column(dbSQL.String(128))
    posts = dbSQL.relationship('Post', backref='author', lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('Password cannot be read directly!')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password, password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    @staticmethod
    def make_valid_nickname(nickname):
        return re.sub('[^a-zA-Z0-9_\.]', '', nickname)

    @staticmethod
    def make_unique_nickname(nickname):
        if Account.query.filter_by(nickname=nickname).first() is None:
            return nickname
        version = 2
        while True:
            new_nickname = nickname + str(version)
            if Account.query.filter_by(nickname=new_nickname).first() is None:
                break
            version += 1
        return new_nickname

    # def __repr__(self):
    #     return '<Account name %r>' % self.name
class Post(dbSQL.Model):
    __tablename__ = 'posts'
    id = dbSQL.Column(dbSQL.Integer, primary_key = True)
    body = dbSQL.Column(dbSQL.String(200))
    timestamp = dbSQL.Column(dbSQL.DateTime)
    user_id = dbSQL.Column(dbSQL.Integer, dbSQL.ForeignKey('accounts.id'))

class Verification():

    def find_existing_user(self):
        return Account.query.filter_by(nickname=self).first()

    def find_user_pwd(self):
        user = find_existing_user(self)
        return user.password_hash

    def find_user_post(self):
        user = find_existing_user(self)
        posts = Post.query.filter_by(user_id=user.id).all()
        return posts


dbSQL.drop_all()
dbSQL.create_all()
admin = Account(nickname='admin',
                 password_hash=generate_password_hash('admin'))

dbSQL.session.add(admin)
dbSQL.session.commit()



# block below is temporarily abandoned
# '''
# # define a User table to store user id, nickname, email and posts
# class Account(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     nickname = db.Column(db.String(64), index=True, unique=True)
#     email = db.Column(db.String(120), index=True, unique=True)
#     postTitle = db.Column(db.String(2000), index=True, unique=True)
#     postBody = db.Column(db.String(2000), index=True, unique=True)
#
#     def __repr__(self):
#         return '<User %r>' % (self.nickname)
# '''


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
