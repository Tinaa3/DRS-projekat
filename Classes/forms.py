from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, IntegerField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError, Regexp
from Classes.User import User

class RegisterForm(FlaskForm):
    name=StringField(label='Name', validators=[Length(min=2, max=30), DataRequired()])
    lastname=StringField(label='Lastname', validators=[Length(min=2, max=30), DataRequired()])
    address=StringField(label='Address', validators=[DataRequired()])
    city=StringField(label='City', validators=[DataRequired()])
    country = StringField(label='Country', validators=[DataRequired()])
    phoneNumber = IntegerField(label='Phone Number', validators=[DataRequired()])
    email=EmailField(label='Email Address', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='password1', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='password2', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account')

class LoginForm(FlaskForm):
    email = EmailField(label='Email', validators=[Email(),DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    submit_login = SubmitField(label='Login')




