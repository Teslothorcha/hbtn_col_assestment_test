
"""
Order model module
"""
from datetime import date, datetime
from app import db, app
from sqlalchemy import event
from decimal import Decimal

from app.models.auditModel import Audit
from app.models.userModel import User
from app.models.productModel import Product


class Order(db.Model, Audit):
    """
    CLass representation of the Order model
    in python level
    """
    __tablename__ = 'order'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    total = db.Column(db.Numeric, nullable=False)
    subtotal = db.Column(db.Numeric, nullable=False)
    taxes = db.Column(db.Numeric, nullable=False)
    paid = db.Column(db.Numeric, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    payments = db.relationship("Payment")
    shipping = db.relationship("Shipping", back_populates="order", uselist=False)
    products = db.relationship(Product,secondary='orderedProduct')

    def __init__(self, total: Decimal, subtotal:Decimal,
                taxes: Decimal, paid:Decimal):
        """
        Initializes a order object
        """
        self.date = date.today()
        self.total = total
        self.subutotal = subtotal
        self.taxes = taxes
        self.paid = paid

    def __repr__(self):
        """
        Provides general information of 
        the order model
        """
        user = db.session.query(User).get(self.user_id)
        return '<order_id: {}, order_date: {}, order_total = {},'\
        ' order_subtotal = {}, order_taxes = {}, order_paid = {},'\
        ' user_id: {}>'.format(
        self.id, self.date, self.total,
        self.subtotal, self.taxes, self.paid, user.id)

@event.listens_for(Order, "after_update")
def order_after_update(mapper, connection, target):
    """
    Sets updated_at attribute to keep object
    trazability.
    """
    order_table = Order.__table__
    connection.execute(
            order_table.update().
             where(order_table.c.id==target.id).
             values(updated_at=datetime.now())
             )
    app.logger.info("register {} with id {} has been updated at {}".\
        format(target.__class__.__tablename__, target.id, target.updated_at))
