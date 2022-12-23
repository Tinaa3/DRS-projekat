from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, IntegerField,PasswordField, SubmitField

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