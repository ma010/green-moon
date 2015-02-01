from GreenMoon import app
from flask.ext.sqlalchemy import SQLAlchemy

## SQL DB for core/structured storage, such as  by organizing or parsing data from MongoDB
# Set up connection with postgresql
dbSQL = SQLAlchemy(app)

from GreenMoon.models import Account

## Initialize dbSQL and and admin
dbSQL.drop_all()
dbSQL.create_all()
admin = Account(name='admin', \
                password_hash=generate_password_hash('admin'))
dbSQL.session.add(admin)
dbSQL.session.commit()


## MongoDB for fast unstructured data storage, such as info crawled from webpages, twitter, etc.
# Set up mongoDB engine
#con = Connection()
# Get database record - businessDB which contains business lincense info
#dbMongo = con.businessDB
