from app import db
from datetime import datetime

class Audit():
    __abstract__ = True

    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    def __init__(self):
        self.created_at = datetime.now()
