"""
This script initializes the database before the web app runs.
PostgresSQL is used as the backend with SQLAlchemy as the API.
"""

from GreenMoon import app, dbSQL
from werkzeug.security import generate_password_hash
from GreenMoon.models import Account

## Initialize dbSQL and admin
dbSQL.drop_all()
dbSQL.create_all()
admin = Account(nickname='admin',
                password_hash=generate_password_hash('admin'))
dbSQL.session.add(admin)
dbSQL.session.commit()