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
from itertools import groupby
from operator import attrgetter
from multiprocessing import Queue, Process

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
    if(email == "" or email.isspace()):
        return redirect(url_for('login_page'))
    password = request.form.get('password')
    if(password == "" or password.isspace()):
        return redirect(url_for('login_page'))
    
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
        if (form.name.data == "" or form.name.data.isspace()
            or form.lastname.data == "" or form.lastname.data.isspace()
            or form.address.data == "" or form.address.data.isspace()
            or form.city.data == "" or form.city.data.isspace()
            or form.country.data == "" or form.country.data.isspace()
            or form.phoneNumber.data == "" or form.phoneNumber.data.isspace()
            or form.email.data == "" or form.email.data.isspace()
            or form.password1.data == "" or form.password1.data.isspace()
            or form.password2.data == "" or form.password2.data.isspace()):
            return redirect(url_for('register_page'))
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
        #table of transactions - 6.
    if request.method=='POST':
        sold_transaction_id = request.form.get('sold_transaction')
        if(sold_transaction_id == None or not sold_transaction_id.isnumeric()):
            return redirect(url_for('profile_page'))
        result_queue = Queue()
        p = Process(target=sell_coin, args=(sold_transaction_id, current_user.id, result_queue))
        p.start()   
        p.join() #wait for this process to complete
        flash(result_queue.get())
    
        #table of coins - 7.
    current_transactions = Transaction.query.filter_by(user_id=current_user.id).all()
    # Group transactions by coin_name
    transactions_by_coin_name = groupby(sorted(current_transactions, key=attrgetter('coin_name')), attrgetter('coin_name'))
    # Sum transactions amount and price for each coin_name
    result = {}
    for coin_name, transactions in transactions_by_coin_name:
        result[coin_name] = {'amount': 0, 'price': 0, 'profit': 0}
        for transaction in transactions:
            result[coin_name]['amount'] += transaction.amount
            result[coin_name]['price'] += transaction.price           
    for key in result.keys():
        current_price = Coin.query.filter_by(symbol=key).first()
        result[key]['profit'] = (current_price.current_value * result[key]['price']) - result[key]['amount']
        
        #sum of coins - 8.
    sum=[0, 0]
    total = 0
    for key in result.keys():
        sum[0] += result[key]['amount']
        sum[1] += result[key]['profit']
        total = sum[0] + sum[1]

        #chart
    plus_profit = 0
    minus_profit = 0
    for key in result.keys():
        if result[key]['profit'] > 0:
            plus_profit += result[key]['profit']
        else:
            minus_profit += result[key]['profit']

    user = User.query.filter_by(id=current_user.id).first()
    transactions = Transaction.query.filter_by(user_id=current_user.id).all()
    return render_template('profile.html', transactions=transactions, user=user, result=result, sum=sum, total=total,  plus_profit=plus_profit, minus_profit=minus_profit)

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
            if(form.name.data == "" or form.name.data.isspace()
                or form.cardnum.data == None or not form.cardnum.data.isnumeric()
                or form.expdate.data == "" or form.name.data.isspace()
                or form.seccode.data == None or not form.seccode.data.isnumeric()
                or form.amount.data == None or not form.amount.data.isnumeric()):
                return redirect(url_for('card_page'))
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
    if(form.name.data != "" and not form.name.data.isspace()):
        userUpdate.name = form.name.data
    if(form.lastname.data != "" and not form.lastname.data.isspace()):
        userUpdate.lastname = form.lastname.data
    if(form.address.data != "" and not form.address.data.isspace()):
        userUpdate.address = form.address.data
    if(form.city.data != "" and not form.city.data.isspace()):
        userUpdate.city = form.city.data
    if(form.country.data != "" and not form.country.data.isspace()):
        userUpdate.country = form.country.data
    if(form.phoneNumber.data != "" and not form.phoneNumber.data.isspace()):
        userUpdate.phoneNumber = form.phoneNumber.data
    if(form.password1.data == form.password2.data 
        and form.password1.data != ""  
        and not form.password1.data.isspace() 
        and form.password2.data != ""
        and not form.password2.data.isspace()):
        userUpdate.password_hash = form.password1.data
    db.session.commit()
    return redirect(url_for('profile_page'))

@app.route('/store', methods=['GET','POST'])
@login_required
def store_page():
    coins = Coin.query.all()
    results = crypto.get_top_200()
    if not coins:
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
        if entered_date == '' and entered_amount == '':
            flash('DATE AND AMOUNT')
            return redirect(url_for('store_page'))
        if entered_date == '':
            flash('Date!')
            return redirect(url_for('store_page'))
        if entered_amount == '':
            flash('Amount!')
            return redirect(url_for('store_page'))
        card = Card.query.filter_by(owner_id=current_user.id).first()
        if card is None:
            result_queue.put('First add credit card!')
            return redirect(url_for('card_page'))
        
        result_queue = Queue()
        p = Process(target=buy_coin, args=(selected_coin, entered_amount, entered_date, current_user.id, result_queue))
        p.start()   
        p.join() #wait for this process to complete
        flash(result_queue.get())
        return redirect(url_for('store_page'))

    return render_template('store.html', results=results, coins=coins)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home_page'))

def sell_coin(sold_transaction_id, current_user_id, result_queue):
    with app.app_context():
        temp_user = User.query.get(int(current_user_id))
        sold_transaction_object = Transaction.query.filter_by(id=sold_transaction_id).first()
        if sold_transaction_object:
            if sold_transaction_object not in temp_user.transactions:
                result_queue.put('Something went wrong! You don\'t have enough' + sold_transaction_object.coin_name + 'to sell.')
                return
            coin_num = sold_transaction_object.price
            coin_object = Coin.query.filter_by(symbol=sold_transaction_object.coin_name).first()
            temp_value = coin_num * coin_object.current_value   
            temp_user.card.amount += temp_value       
            Transaction.query.filter_by(id=sold_transaction_id, user_id=current_user_id).delete()
            db.session.commit()
            result_queue.put('Congratulations! Money from the sale:' + str(temp_value))
        else:
            result_queue.put('Transaction not found')

def buy_coin(selected_coin, entered_amount, entered_date, current_user_id, result_queue):
    with app.app_context():    
        coin = Coin.query.filter_by(symbol=selected_coin).first()
        print(selected_coin)
        print(coin.symbol)
        print(coin.name)
        card = Card.query.filter_by(owner_id=current_user_id).first()
        if coin is not None:
            vr = 0
            try:
                coin = Coin.query.filter_by(symbol=selected_coin).first()
                vr = coin.current_value
            except AttributeError:
                print("Coin not found")
            if vr == 0:
                result_queue.put('Coin is worth zero dollars! The transaction will not be executed.')
                return #redirect(url_for('store_page'))
            res = float(entered_amount) / vr
            new_transaction = Transaction(coin_name = selected_coin, user_id = current_user_id, date=entered_date, amount = entered_amount, price = res)
            if card.amount >= float(entered_amount):
                card.amount -= float(entered_amount)
                db.session.add(new_transaction)
                db.session.commit()
                result_queue.put('Transaction successful')
                return #redirect(url_for('profile_page'))
            else:
                result_queue.put('Not enough funds')
                return #redirect(url_for('store_page'))
        else:
            result_queue.put('Invalid coin')
            return #redirect(url_for('store_page'))