from UI import app
from flask import render_template
from Classes.forms import RegisterForm
from Classes.User import User

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/register')
def register_page():
    form = RegisterForm()
    return render_template('register.html', form=form)
