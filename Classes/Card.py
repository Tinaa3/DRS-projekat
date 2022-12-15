import Classes.User as User

class Card(User.db.Model):
    cardNum=User.db.Column(User.db.String(length=30), nullable=False)
    name=User.db.Column(User.db.String(length=30), nullable=False, primary_key=True)
    dateOfExpires=User.db.Column(User.db.String(length=30), nullable=False)
    secureCode=User.db.Column(User.db.Integer, nullable=False)

    def __repr__(self):
        return f"Card('{self.cardNum}', '{self.name}', '{self.dateOfExpires}', '{self.secureCode}')"

    def __init__(self, cardNum, name, dateOfExpires, secureCode):
        self.cardNum=cardNum
        self.name=name
        self.dateOfExpires=dateOfExpires
        self.secureCode=secureCode


def read(name):
    return Card.query.filter_by(name=name).first()

def add(newCard):
    User.db.session.add(newCard)
    User.db.session.commit()

def delete(name):
    Card.query.filter_by(name=name).delete()
    return