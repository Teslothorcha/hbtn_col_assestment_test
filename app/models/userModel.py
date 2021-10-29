"""
User model module
"""
from datetime import datetime
from sqlalchemy import event
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, app
from app.models.auditModel import Audit


class User(db.Model, Audit, UserMixin):
    """
    Class representation of the User model
    in python level
    """
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    gov_id = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    company = db.Column(db.String, nullable=True)
    orders = db.relationship("Order")
    addresses = db.relationship("Address")
    is_admin = db.Column(db.Boolean, nullable=True)
    password = db.Column(db.Text, nullable=False)
    wallet = db.relationship("Wallet", back_populates="user", uselist=False)
 
    def __init__(self, name: str, last_name: str, gov_id: str,
                email: str, company: str, password:str,
                is_admin: bool=False) -> "User":
        """
        Initilizes a user object
        """
        self.name = name
        self.last_name = last_name
        self.gov_id = gov_id
        self.email = email
        self.company = company
        self.password = self.set_password(password)
        self.is_admin = is_admin

    def __repr__(self):
        """
        Provides general information of
        the user model
        """
        return '<user_id: {}, user_name: {}, user_last_name = {},'\
            ' user_gov_id = {}>'.format(
            self.id, self.name, self.last_name, self.gov_id)

    def set_password(self, password: str):
        """
        Hashes a user password
        """
        return generate_password_hash(password)

    def save_user(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    
    @staticmethod
    def get_user_by_email(email: str)-> "User":
        """
        Get user object by its email
        """
        return db.session.query(User).filter(User.email == email).first()

    @staticmethod
    def get_user_by_id(user_id: int)-> "User":
        """
        Get user object by its email
        """
        return db.session.query(User).get(user_id)

    def validate_password(self, psswd: str)-> bool:
        """
        Validates if password is correct
        """
        return check_password_hash(self.password, psswd)

@event.listens_for(User, "after_update")
def user_after_update(mapper, connection, target):
    """
    Sets updated_at attribute to keep object
    trazability.
    """
    user_table = User.__table__
    connection.execute(
            user_table.update().
             where(user_table.c.id==target.id).
             values(updated_at=datetime.now())
             )
    app.logger.info("register {} has been updated at {}".\
        format(target, target.updated_at))