from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class DisplayForms(FlaskForm):
    user_name  = StringField('UserName', validators=[DataRequired()])
    submit = SubmitField('Updata Data')