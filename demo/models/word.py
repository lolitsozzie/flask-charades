from .base_model import BaseModel
from ..extensions import db


class Word(BaseModel):
    text = db.Column(db.Text, nullable=False)
    categoryId = db.Column(db.Integer, nullable=False)

    @classmethod
    def get_all(cls):
        """
        Get all product variations for a practice
        :return: (list) of ProductVariation objects
        """
        return [w for w in cls.query.all()]