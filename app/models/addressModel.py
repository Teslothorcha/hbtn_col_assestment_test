from datetime import datetime

from app import db#, app
from sqlalchemy import event
from app.models.auditModel import Audit
from app.models.userModel import User


class Address(db.Model, Audit):
    __tablename__ = 'address'

    id = db.Column(db.Integer, primary_key=True)
    main_info = db.Column(db.Text, nullable=False)
    city = db.Column(db.String, nullable=False)
    state = db.Column(db.String, nullable=False)
    country = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    shippings = db.relationship("Shipping")
    
    def __repr__(self):
        user = db.session.query(User).get(self.user_id)
        return '<Adress_id: {}, Adress_ain_info: {}, Adrress_city = {},'\
        ' Adress_state = {}, Address countryy; {}, Usuario: {}>'.format(
        self.id, self.main_info, self.city, self.state,
        self.country, user)

@event.listens_for(Address, "after_update")
def address_after_update(mapper, connection, target):
    address_table = Address.__table__
    connection.execute(
            address_table.update().
             where(address_table.c.id==target.id).
             values(updated_at=datetime.now())
             )
    #app.logger.info("register {} has been updated at {}".\
    #   format(target, target.updated_at))
