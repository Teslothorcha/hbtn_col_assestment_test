from datetime import date

from app import db
from app.models.auditModel import Audit


class Order(db.Model, Audit):
    __tablename__ = 'order'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    total = db.Column(db.Numeric, nullable=False)
    subtotal = db.Column(db.Numeric, nullable=False)
    taxes = db.Column(db.Numeric, nullable=False)
    paid = db.Column(db.Numeric, nullable=False)

    def __init__(self):
        self.date = date.now()
 
    def __repr__(self):
        return '<id: {}, date": {}, total = {}, paid = {}>'.format(
            self.id, self.date, self.total, self.paid)
