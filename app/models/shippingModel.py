from datetime import datetime

from app import db, app
from sqlalchemy import event
from app.models.auditModel import Audit


class Shipping(db.Model, Audit):
    __tablename__ = 'shipping'

    id = db.Column(db.Integer, primary_key=True)
    cost = db.Column(db.Numeric, nullable=False)
    address_id = db.Column(db.Integer, db.ForeignKey('address.id'))
    order = db.relationship("Order", back_populates="shipping", uselist=False)

    def __repr__(self):
        return '<shipping_id: {}, shipping_cost: {}, shipping_address = {},'\
        ' order_order = {}>'.format(
        self.id, self.date, self.total, self.paid)

@event.listens_for(Shipping, "after_update")
def shipping_after_update(mapper, connection, target):
    shipping_table = Shipping.__table__
    connection.execute(
            shipping_table.update().
             where(shipping_table.c.id==target.id).
             values(updated_at=datetime.now())
             )
    app.logger.info("register {} has been updated at {}".\
        format(target, target.updated_at))