from UI import app, db
from flask import render_template, redirect, url_for, flash, request
from Classes.forms import RegisterForm, LoginForm, EditForm
from Classes.User import User
from flask_login import login_user, logout_user, login_required, current_user

@app.route('/')
@app.route('/home', methods=['GET', 'POST'])
def home_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(email=form.email.data).first()
        if attempted_user and attempted_user.password == form.password.data:
            login_user(attempted_user)
            flash(f'You are logged in as: {attempted_user.name}', category='success')
            return redirect(url_for('profile_page'))
        else:
            flash('Email and password do not match!', category='danger')
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
        #login_user(user_to_create)
        flash(f'Account created successufuly! You are now logged in as {user_to_create.name}', category='success')
        return redirect(url_for('profile_page'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')
    return render_template('register.html', form=form)

@app.route('/profile')
def profile_page():
    return render_template('profile.html')

@app.route('/store')
def store_page():
    return render_template('store.html')

@app.route('/editprofile')
def edit_page():
    form = EditForm()
    return render_template('editProfile.html', form=form)