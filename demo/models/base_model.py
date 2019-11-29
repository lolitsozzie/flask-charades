from sqlalchemy import func

from demo.extensions import db


class BaseModel(db.Model):
    """
    Base model used for all models.
    """
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    