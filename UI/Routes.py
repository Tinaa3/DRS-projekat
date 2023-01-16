from UI import app, db
from flask import render_template, redirect, url_for, flash, request
from Classes.forms import RegisterForm, LoginForm, EditForm, CardForm
from Classes.User import User
from Classes.Card import Card
from Classes.Coin import Coin
from Classes.crypto import Crypto
from Classes.Transaction import Transaction
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from flask_login import LoginManager 

crypto = Crypto()
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

@app.route('/', methods=['GET'])
@app.route('/home', methods=['GET'])
def home_page():
    #if request.method=='GET': # if the request is a GET we return the login page
    return render_template('home.html')


@app.route('/', methods=['POST'])   
@app.route('/home', methods=['POST'])   
def login_page():  
    #else: # if the request is POST the we check if the user exist 
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
    flash(f'Welcome {user.name}!')
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
    user = User.query.filter_by(id=current_user.id).first()
    transactions = Transaction.query.filter_by(user_id=current_user.id).all()
    return render_template('profile.html', transactions=transactions, user=user)


@app.route('/card', methods=['GET', 'POST'])
@login_required
def card_page():
    form = CardForm()
    user_id = current_user.id
    cards = Card.query.filter_by(owner_id=user_id).all()
    num_cards = Card.query.filter_by(owner_id=user_id).count()
    if request.method == 'POST':
        if num_cards >= 1:
            
            flash(f"Only one credit card can be added")
            return redirect(url_for('card_page'))
        else:
            card = Card(name=form.name.data,
                        cardNum=form.cardnum.data,
                        expDate=form.expdate.data,
                        secCode=form.seccode.data,
                        amount=form.amount.data,
                        owner_id=user_id)
            db.session.add(card)
            db.session.commit()
            return redirect(url_for('card_page'))

    return render_template('card.html', form=form, cards=cards, num_cards=num_cards)



@app.route('/editprofile', methods=["GET", "POST"])
@login_required
def edit_page():
    form = EditForm()
    if form.is_submitted() is False:
        return render_template('editProfile.html', form=form)
    userUpdate = User.query.filter_by(id=current_user.id).first()
    if(form.name.data != ""):
        userUpdate.name = form.name.data
    if(form.lastname.data != ""):
        userUpdate.lastname = form.lastname.data
    if(form.address.data != ""):
        userUpdate.address = form.address.data
    if(form.city.data != ""):
        userUpdate.city = form.city.data
    if(form.country.data != ""):
        userUpdate.country = form.country.data
    if(form.country.data != ""):
        userUpdate.phoneNumber = form.phoneNumber.data
    if(form.password1.data == form.password2.data and form.password1.data != "" and form.password2.data != ""):
        userUpdate.password_hash = form.password1.data
    db.session.commit()
    return render_template('profile.html')

@app.route('/store', methods=['GET','POST'])
@login_required
def store_page():
    coins = Coin.query.all()
    results = crypto.get_top_200()
    for result in results:
        result['quote']['USD']['price'] = '$ ' + "{:.2f}".format(result['quote']['USD']['price'])
         # Create a Coin object for each coin
        new_coin = Coin(name=result['name'], symbol=result['symbol'],current_value=float(result['quote']['USD']['price'].replace('$','')))
        db.session.add(new_coin)

    db.session.commit()
   
    if request.method == 'POST':
        selected_coin = request.form.get('coin-select')
        entered_amount = request.form.get('money-input')
        entered_date = request.form.get('date-time-input')
        coin = Coin.query.filter_by(name=selected_coin)
        card = Card.query.filter_by(owner_id=current_user.id).first()
        #res = entered_amount / coin.current_value
        print(selected_coin)
        if card is None:
            flash('First add credit card!')
            return redirect(url_for('card_page'))
        else: 
            if coin is not None:
                vr = 0
                try:
                    coin = Coin.query.filter_by(symbol=selected_coin).first()
                    vr = coin.current_value
                except AttributeError:
                    print("Coin not found")

                res = float(entered_amount) / vr
                new_transaction = Transaction(coin_name = selected_coin, user_id = current_user.id,date=entered_date, amount = entered_amount, price = res)
                #card = Card.query.filter_by(owner_id = current_user.id).first()
                if card.amount >= int(entered_amount):
                    card.amount -= int(entered_amount)
                    db.session.add(new_transaction)
                    db.session.commit()
                    flash('Transaction successful')
                    return redirect(url_for('profile_page'))
                else:
                    flash('Not enough funds')
                    return redirect(url_for('store_page'))
            else:
                flash('Invalid coin')
                return redirect(url_for('store_page'))
       
    return render_template('store.html', results=results, coins=coins)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home_page'))