from UI import bcrypt, db, login_manager
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

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

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')
    
    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)