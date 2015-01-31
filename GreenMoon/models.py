from GreenMoon import app
from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy(app)

class Account(db.Model):
    __tablename__ = 'accounts'
    name = db.Column(db.String(12), primary_key=True, unique=True)
    password_hash = db.Column(db.String(128))

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

db.drop_all()
db.create_all()
admin = Account(name='admin', \
                password_hash=generate_password_hash('admin'))
db.session.add(admin)
db.session.commit()
