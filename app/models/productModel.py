from datetime import datetime
from decimal import Decimal

from app import db, app
from sqlalchemy import event
from app.models.auditModel import Audit



class Product(db.Model, Audit):
    __tablename__ = 'product'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    price = db.Column(db.Numeric, nullable=False)
    image_path = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=True)
    orders = db.relationship('Order', secondary = 'orderedProduct')

    def __repr__(self):
        from app.models.orderModel import Order
        order = db.session.query(Order).get(self.order_id)
        return '<product_id: {}, product_name: {}, product_price = {},'\
        ' product_image_path = {}, order_id: {}>'.format(
        self.id, self.name, self.price, self.image_path, order.id)

    def __init__(self, name: str, price: Decimal, image_path: str):
        """
        Initializes a order object
        """
        self.name = name
        self.price = price
        self.image_path = image_path

class OrderedProduct(db.Model, Audit):
    __tablename__ = 'orderedProduct'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(
        db.Integer, 
        db.ForeignKey('product.id'), 
        primary_key = True)

    product_id = db.Column(
    db.Integer, 
    db.ForeignKey('order.id'), 
    primary_key = True)

    def __repr__(self):
        from app.models.orderModel import Order
        order = db.session.query(Order).get(self.order_id)
        product = db.session.query(Product).get(self.product_id)
        
        return '<ordered_product_id: {}, order_id: {}, product_id  = {},'\
        .format(self.id, self.order_id, self.product_id)

@event.listens_for(Product, "after_update")
def product_after_update(mapper, connection, target):
    product_table = Product.__table__
    connection.execute(
            product_table.update().
             where(product_table.c.id==target.id).
             values(updated_at=datetime.now())
             )
    app.logger.info("register {} with id {} has been updated at {}".\
        format(target.__class__.__tablename__, target.id, target.updated_at))


@event.listens_for(OrderedProduct, "after_update")
def payment_after_update(mapper, connection, target):
    ordered_product_table = OrderedProduct.__table__
    connection.execute(
            ordered_product_table.update().
             where(ordered_product_table.c.id==target.id).
             values(updated_at=datetime.now())
             )
    app.logger.info("register {} with id {} has been updated at {}".\
        format(target.__class__.__tablename__, target.id, target.updated_at))