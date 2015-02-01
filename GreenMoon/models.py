from GreenMoon import app, db, dbMongo

# define a User table to store user id, nickname, email and posts
class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    postTitle = db.Column(db.String(2000), index=True, unique=True)
    postBody = db.Column(db.String(2000), index=True, unique=True)

    def __repr__(self):
        return '<User %r>' % (self.nickname)


# define a class Post -- a second database
# to store User's Post separately


# mongdb where business license info is stored
def allTupleFromDB():
    output = ""
    allLicense = dbMongo.activeLicense.find()
    for L in allLicense:
        output += str(L['zip']) + '++'
        temp = ' '.join( str(e) for e in list( L['license'].keys() ) )
        output += temp + '++\t\n'+'++++++++\n'
    return output
