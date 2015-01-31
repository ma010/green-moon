from GreenMoon import app, db, dbSQL

class User(dbSQL.Model):
    id = dbSQL.Column(dbSQL.Integer, primary_key=True)
    nickname = dbSQL.Column(dbSQL.String(64), index=True, unique=True)
    email = dbSQL.Column(dbSQL.String(120), index=True, unique=True)

    def __repr__(self):
        return '<User %r>' % (self.nickname)


# mongdb where business license info is stored
def allTupleFromDB():
    output = ""
    allLicense = db.activeLicense.find()
    for L in allLicense:
        output += str(L['zip']) + '++'
        temp = ' '.join( str(e) for e in list( L['license'].keys() ) )
        output += temp + '++\t\n'+'++++++++\n'
    return output
