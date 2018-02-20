import re
from werkzeug.security import generate_password_hash, check_password_hash
from GreenMoon import app, dbMongo, dbSQL

app.secret_key = 'why would I tell you my secret key?'

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

class Post(dbSQL.Model):

    __tablename__ = 'posts'
    id = dbSQL.Column(dbSQL.Integer, primary_key = True)
    title = dbSQL.Column(dbSQL.String(120), index=True)
    body = dbSQL.Column(dbSQL.String(200))
    timestamp = dbSQL.Column(dbSQL.DateTime)
    user_id = dbSQL.Column(dbSQL.Integer, dbSQL.ForeignKey('accounts.id'))
    nickname = dbSQL.Column(dbSQL.String(50))

    def __init__(self, title, body, timestamp, nickname):
        self.title = title
        self.body = body
        self.timestamp = timestamp
        self.nickname = nickname

    def __repr__(self):
        return '<title {}'.format(self.title)

class Verification():

    def find_existing_user(self):
        return Account.query.filter_by(nickname=self).first()

    def find_user_pwd(self):
        user = Verification.find_existing_user(self)
        return user.password_hash

    def find_user_post(self):
        user = Verification.find_existing_user(self)
        posts = Post.query.filter_by(user_id=user.id).all()
        return posts

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

def licenseFromZip(zipPick):
    output = ""
    temp = ""
    licenseFoundAtZip = dbMongo.activeLicense.find_one({'zip' : str(zipPick)})

    for k, val in licenseFoundAtZip['license'].items():
        temp = str(k) + ': '+ str(val)
        output += temp + '---'
    return output

def licenseTagging(licenseCountAtZip):
    """
    This tagging is only performed to reduce computational complexity,
    Tags are subject to fine tuning, depending on specific analysis.
    :param licenseCountAtZip: a dictionary containing business license tag (as key) and its count (as value)
    :return: taggedLicenseAtZip
    """
    licenseTags = [
        'Diner and bar options', 'Animal Care options', 'Fitness options', 'Market options', 'Gas options',
        'Manufacturing related', 'Outdoor Activity options', 'Garage and Valet options',
        'Motor Vehicle Services', 'Children\'s Services options', 'Tobacco and Liquor',
        'Other Sale options', 'Others'
    ]
    taggedLicenseAtZip = {}

    for k in licenseTags:
        taggedLicenseAtZip[k] = 0

    for k, val in licenseCountAtZip.items():
        if (k =='Music and Dance' or k =='Class A - Indoor Special Event' or 'Food - Shared Kitchen' or
                   k =='Tavern' or k =='Liquor Airport Pushcart License' or
                   k =='Food - Shared Kitchen Long-Term User' or
                   k =='Consumption on Premises - Incidental Activity' or k =='Caterer\'s Liquor License' or
                   k =='Caterer\'s Registration (Liquor)' or k =='Retail Food Establishment' or
                   k =='Food - Shared Kitchen - Supplemental' or k =='Food - Shared Kitchen Short-Term User'):
            taggedLicenseAtZip['Diner and bar options'] += val
        if (k =='Animal Care License'):
            taggedLicenseAtZip['Animal Care options'] += val
        if (k =='Explosives, Certificate of Fitness'):
            taggedLicenseAtZip['Fitness options'] += val
        if (k =='Wholesale Food Establishment' or k =='Mobile Food License' or k =='Package Goods' or
                   k =='Itinerant Merchant' or k =='Peddler License'):
            taggedLicenseAtZip['Market options'] += val
        if (k =='Filling Station'):
            taggedLicenseAtZip['Gas options'] += val
        if (k =='Bicycle Messenger Service' or k =='Manufacturing Establishments'):
            taggedLicenseAtZip['Manufacturing related'] += val
        if (k =='Outdoor Patio' or k =='Navy Pier Kiosk License' or k =='Public Place of Amusement' or
                   k =='Wrigley Field' or k =='Navy Pier - Mobile'):
            taggedLicenseAtZip['Outdoor Activity options'] += val
        if (k =='Accessory Garage' or k =='Public Garage' or k =='Valet Parking Operator'):
            taggedLicenseAtZip['Garage and Valet options'] += val
        if (k =='Motor Vehicle Services License'):
            taggedLicenseAtZip['Motor Vehicle Services'] += val
        if (k =='Children\'s Services Facility License'):
            taggedLicenseAtZip['Children\'s Services options'] += val
        if (k =='Tobacco Retail Over Counter' or k =='Tobacco Sampler' or k =='Tobacco Dealer Wholesale'):
            taggedLicenseAtZip['Tobacco and Liquor'] += val
        if (k =='License Broker' or k =='Secondhand Dealer (Includes Valuable Objects)' or
                   k =='Secondhand Dealer (No Valuable Objects)'):
            taggedLicenseAtZip['Other Sale options'] += val
        else:
            taggedLicenseAtZip['Others'] += val

    return taggedLicenseAtZip


def licenseRecommender(zipPick):
    output = ""
    licenseFoundAtZip = dbMongo.activeLicense.find_one({'zip' : str(zipPick)})
    originalLicenseAtZip = (licenseFoundAtZip['license'])
    taggedLicenseAtZip = licenseTagging(originalLicenseAtZip)

    existingLicenses = list(taggedLicenseAtZip.keys())
    # This part of the code is harded code for now, will compute these frequent pairs
    # on server and create a new businessDB.freq collection.
    list1 = [['Diner and bar options'], ['Market options'], ['Others']]
    list2 = [
        ['Diner and bar options', 'Animal Care options'], ['Diner and bar options', 'Market options'],
        ['Diner and bar options', 'Gas options'], ['Diner and bar options', 'Manufacturing related'],
        ['Diner and bar options', 'Outdoor Activity options'],
        ['Diner and bar options', 'Garage and Valet options'],
        ['Diner and bar options', 'Motor Vehicle Services'],
        ['Diner and bar options', "Children's Services options"],
        ['Diner and bar options', 'Tobacco and Liquor'],
        ['Diner and bar options', 'Other Sale options'],
        ['Diner and bar options', 'Others'],
        ['Animal Care options', 'Market options'],
        ['Animal Care options', 'Gas options'],
        ['Animal Care options', 'Manufacturing related'],
        ['Animal Care options', 'Outdoor Activity options'],
        ['Animal Care options', 'Garage and Valet options'],
        ['Animal Care options', 'Motor Vehicle Services'],
        ['Animal Care options', "Children's Services options"],
        ['Animal Care options', 'Tobacco and Liquor'],
        ['Animal Care options', 'Other Sale options'],
        ['Animal Care options', 'Others'], ['Market options', 'Gas options'],
        ['Market options', 'Manufacturing related'], ['Market options', 'Outdoor Activity options'],
        ['Market options', 'Garage and Valet options'], ['Market options', 'Motor Vehicle Services'],
        ['Market options', "Children's Services options"], ['Market options', 'Tobacco and Liquor'],
        ['Market options', 'Other Sale options'], ['Market options', 'Others'],
        ['Gas options', 'Manufacturing related'], ['Gas options', 'Outdoor Activity options'],
        ['Gas options', 'Garage and Valet options'], ['Gas options', 'Motor Vehicle Services'],
        ['Gas options', "Children's Services options"], ['Gas options', 'Tobacco and Liquor'],
        ['Gas options', 'Other Sale options'], ['Gas options', 'Others'],
        ['Manufacturing related', 'Outdoor Activity options'],
        ['Manufacturing related', 'Garage and Valet options'],
        ['Manufacturing related', 'Motor Vehicle Services'],
        ['Manufacturing related', "Children's Services options"],
        ['Manufacturing related', 'Tobacco and Liquor'],
        ['Manufacturing related', 'Other Sale options'],
        ['Manufacturing related', 'Others'], ['Outdoor Activity options', 'Garage and Valet options'],
        ['Outdoor Activity options', 'Motor Vehicle Services'],
        ['Outdoor Activity options', "Children's Services options"],
        ['Outdoor Activity options', 'Tobacco and Liquor'],
        ['Outdoor Activity options', 'Other Sale options'],
        ['Outdoor Activity options', 'Others'], ['Garage and Valet options', 'Motor Vehicle Services'],
        ['Garage and Valet options', "Children's Services options"],
        ['Garage and Valet options', 'Tobacco and Liquor'], ['Garage and Valet options', 'Other Sale options'],
        ['Garage and Valet options', 'Others'], ['Motor Vehicle Services', "Children's Services options"],
        ['Motor Vehicle Services', 'Tobacco and Liquor'], ['Motor Vehicle Services', 'Other Sale options'],
        ['Motor Vehicle Services', 'Others'], ["Children's Services options", 'Tobacco and Liquor'],
        ["Children's Services options", 'Other Sale options'], ["Children's Services options", 'Others'],
        ['Tobacco and Liquor', 'Other Sale options'], ['Tobacco and Liquor', 'Others'],
        ['Other Sale options', 'Others']
    ]

    list3 = [['Diner and bar options', 'Market options', 'Others']]
    licenseRec = []

    for L in list1:
        if(L[0] not in existingLicenses):
            licenseRec.append(L[0])

    for c in list2:
        if(c[0] in existingLicenses and c[1] not in existingLicenses and c[1] not in licenseRec):
            licenseRec.append(c[1])
        if(c[1] in existingLicenses and c[0] not in existingLicenses and c[0] not in licenseRec):
            licenseRec.append(c[0])
        if(c[0] not in existingLicenses and c[1] not in existingLicenses and
                   c[0] not in licenseRec and c[1] not in licenseRec):
            licenseRec.append(c[0])
            licenseRec.append(c[1])

    for t in list3:
        for t_l in t:
            if(t_l not in existingLicenses and t_l not in licenseRec):
                licenseRec.append(t_l)

    return licenseRec

