from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

class LoginForms(FlaskForm):
    user_name  = StringField('User Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])    
    submit = SubmitField('Sign In')