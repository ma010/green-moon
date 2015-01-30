#! /usr/bin/python

import sys
import logging

logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, "/var/www/FlaskApp/")

from GreenMoon import app as application
application.secret_key = "asldfkjasldkfj.,asdf,asdfasjj!!w48rasdflkj__1234q4w5jjfasdf!)(&KHLKJHF!(*&^@%!)*&^!%%%!!KJHAG"
