import bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from UI import db
from flask_login import UserMixin

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


    