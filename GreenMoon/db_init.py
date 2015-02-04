from GreenMoon import app
from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
## SQL DB for core/structured storage, such as  by organizing or parsing data from MongoDB
# Set up connection with postgresql
dbSQL = SQLAlchemy(app)

from GreenMoon.models import Account

## Initialize dbSQL and add "admin:admin" as a user
## NOTE: ONLY RUN THIS ON THE FIRST GO, DELETE LINES 12-16 AFTERWARDS.
'''dbSQL.drop_all()
dbSQL.create_all()
admin = Account(nickname='admin', password_hash=generate_password_hash('admin'))
dbSQL.session.add(admin)
dbSQL.session.commit()'''


## MongoDB for fast unstructured data storage, such as info crawled from webpages, twitter, etc.
# Set up mongoDB engine
#con = Connection()
# Get database record - businessDB which contains business lincense info
#dbMongo = con.businessDB
