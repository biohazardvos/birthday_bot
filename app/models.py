from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    b_date = db.Column(db.String(10), index=True)

    def __repr__(self):
        return '{}'.format(self.b_date)
