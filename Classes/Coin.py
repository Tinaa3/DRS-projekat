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

