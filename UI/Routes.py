from UI import app, db
from flask import render_template, redirect, url_for, flash, request
from Classes.forms import RegisterForm, LoginForm
from Classes.User import User
from flask_login import login_user, logout_user, login_required, current_user

@app.route('/')
@app.route('/home', methods=['GET', 'POST'])
def home_page():
    form = LoginForm()
    return render_template('home.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(name=form.name.data,
                                lastname=form.lastname.data,
                                address=form.address.data,
                                city=form.city.data,
                                country=form.country.data,
                                phoneNumber=form.phoneNumber.data,
                                email=form.email.data,
                                password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f'Account created successufuly! You are now logged in as {user_to_create.name}', category='success')
        return redirect(url_for('profile_page'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')
    return render_template('register.html', form=form)

@app.route('/profile')
def profile_page():
    return render_template('profile.html')