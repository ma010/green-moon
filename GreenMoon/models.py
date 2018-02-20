"""

"""

import re
from werkzeug.security import generate_password_hash, check_password_hash
from GreenMoon import app, dbMongo, dbSQL

app.secret_key = 'why would I tell you my secret key?'


class Account(dbSQL.Model):
    """
    Create user account with id, nickname, password, and associated posts from the user
    """
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
    """
    Create SQL database schema model
    """
    __tablename__ = 'posts'
    id = dbSQL.Column(dbSQL.Integer, primary_key=True)
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


class Verification:
    """
    Verify a user's information during registration, login.
    And find relevant posts from the user.
    """

    def find_existing_user(self):
        return Account.query.filter_by(nickname=self).first()

    def find_user_pwd(self):
        user = Verification.find_existing_user(self)
        return user.password_hash

    def find_user_post(self):
        user = Verification.find_existing_user(self)
        posts = Post.query.filter_by(user_id=user.id).all()
        return posts


# Needs more input from Bo
# Define a method to draw data from MongoDB and then print
def get_license_zip():
    """
    Get (license, zipcode) tuple form database
    :return: all business license and zipcode pairs
    """
    output = ""
    all_license = dbMongo.activeLicense.find()

    for L in all_license:
        output += str(L['zip']) + '++'
        temp = ' '.join(str(e) for e in list(L['license'].keys()))
        output += temp + '++\t\n' + '++++++++\n'
    return output


def license_from_zip(zip_pick):
    """
    Get all the business licenses within the zipcode area given or picked by a user
    :param zip_pick: zipcode (integer) picked or input by a user
    :return: a list of licenses in the zipcode area specified by a user
    """
    output = ""
    license_found_at_zip = dbMongo.activeLicense.find_one({'zip': str(zip_pick)})

    for k, val in license_found_at_zip['license'].items():
        temp = str(k) + ': ' + str(val)
        output += temp + '---'
    return output


def license_tagging(license_count_at_zip):
    """
    This tagging is only performed to reduce computational complexity,
    Tags are subject to fine tuning, depending on specific analysis.
    :param license_count_at_zip: a dictionary containing business license tag (as key) and its count (as value)
    :return: a dictionary of tagged licenses at a particular zipcode area
    """
    license_tags = [
        'Diner and bar options', 'Animal Care options', 'Fitness options', 'Market options', 'Gas options',
        'Manufacturing related', 'Outdoor Activity options', 'Garage and Valet options',
        'Motor Vehicle Services', 'Children\'s Services options', 'Tobacco and Liquor',
        'Other Sale options', 'Others'
    ]
    tagged_license_at_zip = {}

    for k in license_tags:
        tagged_license_at_zip[k] = 0

    for k, val in license_count_at_zip.items():
        if (k == 'Music and Dance' or k == 'Class A - Indoor Special Event' or 'Food - Shared Kitchen' or
                    k == 'Tavern' or k == 'Liquor Airport Pushcart License' or
                    k == 'Food - Shared Kitchen Long-Term User' or
                    k == 'Consumption on Premises - Incidental Activity' or k == 'Caterer\'s Liquor License' or
                    k == 'Caterer\'s Registration (Liquor)' or k == 'Retail Food Establishment' or
                    k == 'Food - Shared Kitchen - Supplemental' or k == 'Food - Shared Kitchen Short-Term User'):
            tagged_license_at_zip['Diner and bar options'] += val
        if (k == 'Animal Care License'):
            tagged_license_at_zip['Animal Care options'] += val
        if (k == 'Explosives, Certificate of Fitness'):
            tagged_license_at_zip['Fitness options'] += val
        if (k == 'Wholesale Food Establishment' or k == 'Mobile Food License' or k == 'Package Goods' or
                    k == 'Itinerant Merchant' or k == 'Peddler License'):
            tagged_license_at_zip['Market options'] += val
        if (k == 'Filling Station'):
            tagged_license_at_zip['Gas options'] += val
        if (k == 'Bicycle Messenger Service' or k == 'Manufacturing Establishments'):
            tagged_license_at_zip['Manufacturing related'] += val
        if (k == 'Outdoor Patio' or k == 'Navy Pier Kiosk License' or k == 'Public Place of Amusement' or
                    k == 'Wrigley Field' or k == 'Navy Pier - Mobile'):
            tagged_license_at_zip['Outdoor Activity options'] += val
        if (k == 'Accessory Garage' or k == 'Public Garage' or k == 'Valet Parking Operator'):
            tagged_license_at_zip['Garage and Valet options'] += val
        if (k == 'Motor Vehicle Services License'):
            tagged_license_at_zip['Motor Vehicle Services'] += val
        if (k == 'Children\'s Services Facility License'):
            tagged_license_at_zip['Children\'s Services options'] += val
        if (k == 'Tobacco Retail Over Counter' or k == 'Tobacco Sampler' or k == 'Tobacco Dealer Wholesale'):
            tagged_license_at_zip['Tobacco and Liquor'] += val
        if (k == 'License Broker' or k == 'Secondhand Dealer (Includes Valuable Objects)' or
                    k == 'Secondhand Dealer (No Valuable Objects)'):
            tagged_license_at_zip['Other Sale options'] += val
        else:
            tagged_license_at_zip['Others'] += val

    return tagged_license_at_zip


def license_recommender(zip_pick):
    """
    Recommend new business entities to a particular zip-code area based on business association analysis
    :param zip_pick: a zipcode integer
    :return: a list of recommended types of business license
    """
    license_found_at_zip = dbMongo.activeLicense.find_one({'zip': str(zip_pick)})
    original_license_at_zip = (license_found_at_zip['license'])
    tagged_license_at_zip = license_tagging(original_license_at_zip)

    existing_licenses = list(tagged_license_at_zip.keys())
    # This part of the code is hard coded for now, will compute these frequent pairs
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
    license_rec = []

    for L in list1:
        if L[0] not in existing_licenses:
            license_rec.append(L[0])

    for c in list2:
        if c[0] in existing_licenses and c[1] not in existing_licenses and c[1] not in license_rec:
            license_rec.append(c[1])
        if c[1] in existing_licenses and c[0] not in existing_licenses and c[0] not in license_rec:
            license_rec.append(c[0])
        if c[0] not in existing_licenses and c[1] not in existing_licenses and c[0] not in license_rec \
                and c[1] not in license_rec:
            license_rec.append(c[0])
            license_rec.append(c[1])

    for t in list3:
        for t_l in t:
            if t_l not in existing_licenses and t_l not in license_rec:
                license_rec.append(t_l)

    return license_rec
