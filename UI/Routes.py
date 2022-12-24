from UI import app
from flask import render_template, redirect, url_for, flash, request
from Classes.forms import RegisterForm, LoginForm
from Classes.User import User
from flask_login import login_user, logout_user, login_required, current_user

@app.route('/')
@app.route('/home', methods=['GET', 'SET'])
def home_page():
    form = LoginForm()
    return render_template('home.html', form=form)

@app.route('/register', methods=['GET', 'SET'])
def register_page():
    form = RegisterForm()
    return render_template('register.html', form=form)
