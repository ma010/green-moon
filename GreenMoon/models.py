from GreenMoon import app
from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

dbSQL = SQLAlchemy(app)

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

dbSQL.drop_all()
dbSQL.create_all()
admin = Account(name='admin', \
                password_hash=generate_password_hash('admin'))
dbSQL.session.add(admin)
dbSQL.session.commit()
