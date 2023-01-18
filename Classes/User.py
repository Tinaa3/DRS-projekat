import bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from UI import db
from flask_login import UserMixin

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable = False)
    lastname = db.Column(db.String(length=30), nullable = False)
    address = db.Column(db.String(length=30), nullable = False)
    city = db.Column(db.String(length=30), nullable = False)
    country = db.Column(db.String(length=30), nullable = False)
    phoneNumber = db.Column(db.String(length=10), nullable = False)
    email = db.Column(db.String(length=50), nullable = False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    transactions = db.relationship('Transaction', backref='user', lazy=True)
    card = db.relationship('Card', uselist=False, back_populates='owner')

    #@property
    #def password(self):
    #    return self.password

    #@password.setter
    #def password(self, plain_text_password):
     #   self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')
    
    #def check_password_correction(self, attempted_password):
     #   return bcrypt.check_password_hash(self.password_hash, attempted_password)


    