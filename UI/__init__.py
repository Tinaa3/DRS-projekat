from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY']='73996d0dcd212694ba3e8d39'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)



from UI import Routes
from Classes.User import  User

