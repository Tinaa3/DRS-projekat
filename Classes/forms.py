from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, IntegerField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from Classes.User import User

class RegisterForm(FlaskForm):
    name=StringField(label='Name')
    lastname=StringField(label='Lastname')
    address=StringField(label='Address')
    city=StringField(label='City')
    country = StringField(label='Country')
    phoneNumber = IntegerField(label='Phone Number')
    email=EmailField(label='Email Address')
    password1 = PasswordField(label='password1')
    password2 = PasswordField(label='password2')
    submit = SubmitField(label='Create Account')

class LoginForm(FlaskForm):
    username = StringField(label='Username', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    submit = SubmitField(label='Sign in')




