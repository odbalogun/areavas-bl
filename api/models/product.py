from . import db
from .abc import BaseModel


class Category(db.Model, BaseModel):
    __tablename__ = 'categories'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    slug = db.Column(db.String(100), unique=True)
    paystack_price = db.Column(db.Integer)  # measured in kobo
    vas_price = db.Column(db.Integer)  # measured in kobo
    validity = db.Column(db.Integer)
    paystack_plan_id = db.Column(db.String(100))  # Paystack subscription code

    def __repr__(self):
        return self.name
