#!venv/bin/python
from GreenMoon import app as application
# ----------
# The above code can be put into a file called GreenMoon.wsgi for Apache deployment
application.run(debug=True)

