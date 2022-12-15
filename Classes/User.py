from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
#db.create_all()

class User(db.Model):
    name = db.Column(db.String(length=30), nullable = False)
    lastname = db.Column(db.String(length=30), nullable = False)
    address = db.Column(db.String(length=30), nullable = False)
    city = db.Column(db.String(length=30), nullable = False)
    country = db.Column(db.String(length=30), nullable = False)
    phoneNumber = db.Column(db.String(length=10), nullable = False)
    email = db.Column(db.String(length=50), nullable = False, primary_key=True, unique=True)
    password = db.Column(db.String(length=50), nullable = False)

    def __repr__(self):
        return f"User('{self.name}', '{self.lastname}', {self.address}, '{self.city}', '{self.country}', '{self.phoneNumber}', '{self.email}', '{self.password}')"

    def __init__(self, name, lastname, address, city, country, phoneNumber, email, password):
        self.name = name
        self.lastname = lastname
        self.address = address
        self.city = city
        self.country = country
        self.phoneNumber = phoneNumber
        self.email = email
        self.password = password

def read(emailAddress):
    return User.query.filter_by(email=emailAddress).first()

def add(newUser, flag):
    if flag:
        db.session.add(newUser)
    db.session.commit()

def delete(emailAddress):
    User.query.filter_by(email=emailAddress).delete()
    return