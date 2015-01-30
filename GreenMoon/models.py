from GreenMoon import app, db

def allTupleFromDB():
    output = ""
    allLicense = db.activeLicense.find()
    for L in allLicense:
        output += str(L['zip']) + '++'
        temp = ' '.join( str(e) for e in list( L['license'].keys() ) )
        output += temp + '++\t\n'+'++++++++\n'
    return output
