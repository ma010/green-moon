"""
    Implement a class function for user to put in a zip-code and
    search relevant information about business entities in that zip-code area.
"""

from flask.ext.wtf import Form
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired

class inputZipForm(Form):
    inputZip = StringField('inputZip', validators=[DataRequired()])

