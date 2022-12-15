import Classes.User as User

class Transaction(User.db.Model):
    sender=User.db.Column(User.db.String(length=30), nullable=False)
    recipient=User.db.Column(User.db.String(length=30), nullable=False)
    amount=User.db.Column(User.db.String(length=30), nullable=False)
    randomInt=User.db.Column(User.db.Integer, nullable=False)
    state=User.db.Column(User.db.String(length=30), nullable=False)
    hashId=User.db.Column(User.db.Integer, nullable=False, primary_key=True)

    def __repr__(self):
        return f"Transaction('{self.sender}', '{self.recipient}', '{self.amount}', '{self.randomInt}', '{self.cardNum}', '{self.state}', '{self.hashId}')"

    def __init__(self, sender, recipient, amount, randomInt, state, hashId):
        self.sender=sender
        self.recipient=recipient
        self.amount=amount
        self.randomInt=randomInt
        self.state=state
        self.hashId=hashId

def read(hashId):
    return Transaction.query.filter_by(hashId=hashId).first()

def add(newTransaction, flag):
    if flag:
        User.db.session.add(newTransaction)
    User.db.session.commit()

def delete(hashId):
    Transaction.query.filter_by(hashId=hashId).delete()
    return