from flask.ext.wtf import Form
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired


class inputZipForm(Form):
    inputZip = StringField('inputZip', validators=[DataRequired()])
