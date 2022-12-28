from UI import app, db
from flask import render_template, redirect, url_for, flash, request
from Classes.forms import RegisterForm, LoginForm, EditForm
from Classes.User import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from flask_login import LoginManager

login_manager = LoginManager() # Create a Login Manager instance
login_manager.login_view = 'home_page' # define the redirection 
                         # path when login required and we attempt 
                         # to access without being logged in
login_manager.init_app(app) # configure it for login

@login_manager.user_loader
def load_user(user_id): #reload user object from the user ID 
                            #stored in the session
        # since the user_id is just the primary key of our user 
        # table, use it in the query for the user
    return User.query.get(int(user_id))

@app.route('/', methods=['GET','POST'])
@app.route('/home', methods=['GET','POST'])
def home_page():
    if request.method=='GET': # if the request is a GET we return the login page
        return render_template('home.html')
    else: # if the request is POST the we check if the user exist 
          # and with te right password
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        
        if not user or (user.password_hash != password):
            flash('Please enter valid login information!')
            return redirect(url_for('home_page'))
       
         # if the user 
               #doesn't exist or password is wrong, reload the page
        # if the above check passes, then we know the user has the 
        # right credentials
        login_user(user)
        flash(f'You are now logged in as {user.name}')
        return redirect(url_for('profile_page'))
    
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
                                password_hash=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f'Account created successufuly! You are now logged in as {user_to_create.name}', category='success')
        return redirect(url_for('profile_page'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')
    return render_template('register.html', form=form)

@app.route('/profile', methods=['GET','POST'])
@login_required
def profile_page():
    return render_template('profile.html')

@app.route('/store')
def store_page():
    return render_template('store.html')

@app.route('/editprofile')
def edit_page():
    form = EditForm()
    return render_template('editProfile.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home_page'))