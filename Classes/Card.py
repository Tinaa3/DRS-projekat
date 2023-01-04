import Classes.User as User
from UI import db


class Card(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable = False)
    cardNum = db.Column(db.Integer(),unique=True, nullable = False)
    expDate = db.Column(db.String(length=8), nullable = False)
    secCode = db.Column(db.Integer(), nullable = False)
    amount = db.Column(db.Integer(), nullable = False)
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))
    
