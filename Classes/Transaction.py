from UI import db

class Transaction(db.Model):
    id = db.Column(db.Integer(), primary_key=True, nullable = False)
    coin_name = db.Column(db.String(), db.ForeignKey('coin.name'), nullable = False)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable = False)
    date = db.Column(db.String(), nullable = False)
    amount = db.Column(db.Float(), nullable=False)
    price = db.Column(db.Float(), nullable = False)


