# Import
#from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from flask import Flask

# Create the application, __name__ tells Flask the root dir of the web app 
app = Flask(__name__)

# Load configuration
# from_object(): load all uppercase variables from object
# from_envvar(): load config from file defined by environment variable
# from_pyfile(): load config from file
app.config.from_pyfile('config.py')

# Load module view to render pages
from GreenMoon import views
# Load module models for database
from GreenMoon import models

# run a flask server if this file is executed directly
if __name__ == '__main__':
    app.run(debug=TRUE)
