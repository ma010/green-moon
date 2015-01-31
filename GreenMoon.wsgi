# Apache + mod_wsgi
# This file will be executed by mod_wsgi on startup to get the application object
# If the application is not on the python load path, add it to system path first like this:
#   import sys
#   sys.path.insert(0, '/path/to/the/application')
from daisygarden import app as application
