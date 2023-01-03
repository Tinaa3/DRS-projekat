from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, IntegerField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError, Regexp, NumberRange
from Classes.User import User

class RegisterForm(FlaskForm):
    name=StringField(label='Name', validators=[Length(min=2, max=30), DataRequired()])
    lastname=StringField(label='Lastname', validators=[Length(min=2, max=30), DataRequired()])
    address=StringField(label='Address', validators=[DataRequired()])
    city=StringField(label='City', validators=[DataRequired()])
    country = StringField(label='Country', validators=[DataRequired()])
    phoneNumber = StringField(label='Phone Number', validators=[DataRequired()])
    email=EmailField(label='Email Address', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='password1', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='password2', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account')

class LoginForm(FlaskForm):
    email = EmailField(label='Email', validators=[Email(),DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    submit = SubmitField(label='Login')


class CardForm(FlaskForm):
    name = StringField('Cardholder name', validators=[DataRequired(), Length(min=15,max=30)])
    cardnum = StringField('Card number', validators=[DataRequired(), Length(min=13, max=16), Regexp('^[0-9]*$', message='Card number must be numeric')])
    expdate = StringField('Expiration date', validators=[DataRequired(), Length(min=4,max=4), Regexp('^(0[1-9]|1[0-2])([0-9]{2})$', message='Expiration date must be in the format MMYY')])
    seccode = IntegerField('Security code', validators=[DataRequired(), NumberRange(min=100, max=999)])
    amount = IntegerField('Amount', validators=[DataRequired(), Length(min=4, max=8)])
    submit = SubmitField(label='submit')

class EditForm(FlaskForm):
    name=StringField(label='Name', validators=[Length(min=2, max=30)])
    lastname=StringField(label='Lastname', validators=[Length(min=2, max=30)])
    address=StringField(label='Address')
    city=StringField(label='City')
    country = StringField(label='Country')
    phoneNumber = StringField(label='Phone Number')
    password1 = PasswordField(label='password1')
    password2 = PasswordField(label='password2')
    submit = SubmitField(label='Edit Account')