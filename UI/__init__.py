from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY']='73996d0dcd212694ba3e8d39'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager()
#login_manager.login_view = 'profile_page'
login_manager.init_app(app)


from UI import Routes
from Classes.User import  User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))