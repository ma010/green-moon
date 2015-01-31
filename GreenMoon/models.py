from GreenMoon import app, db, dbSQL

# define a User table to store user id, nickname, email and posts
class User(dbSQL.Model):
    id = dbSQL.Column(dbSQL.Integer, primary_key=True)
    nickname = dbSQL.Column(dbSQL.String(64), index=True, unique=True)
    email = dbSQL.Column(dbSQL.String(120), index=True, unique=True)
    postTitle = dbSQL.Column(dbSQL.String(2000), index=True, unique=True)
    postBody = dbSQL.Column(dbSQL.String(2000), index=True, unique=True)

    def __repr__(self):
        return '<User %r>' % (self.nickname)


# define a class Post -- a second database
# to store User's Post separately



# mongdb where business license info is stored
def allTupleFromDB():
    output = ""
    allLicense = db.activeLicense.find()
    for L in allLicense:
        output += str(L['zip']) + '++'
        temp = ' '.join( str(e) for e in list( L['license'].keys() ) )
        output += temp + '++\t\n'+'++++++++\n'
    return output
