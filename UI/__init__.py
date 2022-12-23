from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY']='73996d0dcd212694ba3e8d39'
db = SQLAlchemy(app)

from UI import Routes
from Classes import Card, User, Transaction