from datetime import datetime

from app import db, app
from sqlalchemy import event
from app.models.auditModel import Audit


class Shipping(db.Model, Audit):
    __tablename__ = 'shipping'

    id = db.Column(db.Integer, primary_key=True)
    cost = db.Column(db.Numeric, nullable=False)
    address_id = db.Column(db.Integer, db.ForeignKey('address.id'))
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    order = db.relationship("Order", back_populates="shipping")

    def __repr__(self):
        return '<shipping_id: {}, shipping_cost: {}, shipping_address_id = {},'\
        ' shipping_order_id = {}>'.format(
        self.id, self.cost, self.address_id, self.order_id)

@event.listens_for(Shipping, "after_update")
def shipping_after_update(mapper, connection, target):
    shipping_table = Shipping.__table__
    connection.execute(
            shipping_table.update().
             where(shipping_table.c.id==target.id).
             values(updated_at=datetime.now())
             )
    app.logger.info("register {} with id {} has been updated at {}".\
        format(target.__class__.__tablename__, target.id, target.updated_at))