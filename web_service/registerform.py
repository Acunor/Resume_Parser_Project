# from flask_wtf import FlaskForm
# from wtforms.validators import DataRequired
# from wtforms import Form, BooleanField, StringField, PasswordField, validators, SubmitField

# class RegistrationForm(FlaskForm):
#     user_name = StringField('Username', [validators.Length(min=4, max=25)])
#     email = StringField('Email Address', [validators.Length(min=6, max=35)])
#     password = PasswordField('New Password', [validators.DataRequired(),
#         validators.EqualTo('confirm', message='Passwords must match')])
#     confirm = PasswordField('Repeat Password')
#     accept_tos = BooleanField('I accept the TOS', [validators.DataRequired()])
#     submit = SubmitField('Sign In')

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

class RegisterForms(FlaskForm):
    user_name  = StringField('UserName', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')