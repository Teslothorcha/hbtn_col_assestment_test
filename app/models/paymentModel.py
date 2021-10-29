from datetime import datetime
from decimal import Decimal

from app import db, app
from sqlalchemy import event
from app.models.auditModel import Audit
from app.models.orderModel import Order
from app.models.userModel import User


class Payment(db.Model, Audit):
    __tablename__ = 'payment'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    total = db.Column(db.Numeric, nullable=False)
    status = db.Column(db.Boolean, nullable=False)
    txn_id = db.Column(db.Text, nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))

    def __repr__(self):
        order = db.session.query(Order).get(self.order_id)
        return '<payment_id: {}, payment_date: {}, payment_total = {},'\
        ' payment_status = {}, payment_txn_id: {}, payment_order_id = {}>'.format(
        self.id, self.date, self.total, self.payment_status,
        self.pyment_txn_id, order.id)

class Wallet(db.Model, Audit):
    __tablename__ = 'wallet'

    id = db.Column(db.Integer, primary_key=True)
    balance = db.Column(db.Numeric, nullable=False)
    user = db.relationship("User", back_populates="wallet")

    def __init__(self, balance: Decimal, user: User) -> "Wallet":
        """
        Initilizes a wallet object
        """
        self.balance = balance
        self.user = user

    def __repr__(self):
        user = db.session.query(Order).get(self.user)
        return '<wallet_id: {}, wallet_balance: {}, wallet_user_id = {},'\
        .format(self.id, self.balance, self.user_id)

    def save_wallet(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

@event.listens_for(Payment, "after_update")
def payment_after_update(mapper, connection, target):
    payment_table = Payment.__table__
    connection.execute(
            payment_table.update().
             where(payment_table.c.id==target.id).
             values(updated_at=datetime.now())
             )
    app.logger.info("register {} with id {} has been updated at {}".\
        format(target.__class__.__tablename__, target.id, target.updated_at))

@event.listens_for(Wallet, "after_update")
def wallet_after_update(mapper, connection, target):
    wallet_table = Wallet.__table__
    connection.execute(
            wallet_table.update().
             where(wallet_table.c.id==target.id).
             values(updated_at=datetime.now())
             )
    app.logger.info("register {} with id {} has been updated at {}".\
        format(target.__class__.__tablename__, target.id, target.updated_at))
