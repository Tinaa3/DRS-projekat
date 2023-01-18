from UI import db
from Classes import crypto
import schedule
import time

class Coin(db.Model):
    id = db.Column(db.Integer(), primary_key=True, nullable = False)
    symbol = db.Column(db.String(255), nullable =False)
    name = db.Column(db.String(), nullable = False)
    #price = db.Column(db.Integer(),nullable=False)
    current_value = db.Column(db.Float(), nullable = False)
    transactions = db.relationship('Transaction', backref='coin', lazy=True)
    
def update_coin_values():
    coins = Coin.query.all()
    for coin in coins:
        symbol = coin.symbol
        current_price = crypto.get_coin_price(symbol) 
        coin.current_value = current_price
    db.session.commit()

schedule.every(5).hours.do(update_coin_values)
