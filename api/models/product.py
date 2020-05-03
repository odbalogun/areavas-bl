from . import db
from .abc import BaseModel


class Product(db.Model, BaseModel):
    __tablename__ = 'products'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    slug = db.Column(db.String(100), unique=True)

    def __repr__(self):
        return self.name


class ProductCategory(db.Model, BaseModel):
    __tablename__ = 'product_categories'

    id = db.Column(db.Integer(), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    name = db.Column(db.String(80), unique=True)
    slug = db.Column(db.String(100), unique=True)
    price = db.Column(db.Integer)  # measured in kobo
    validity = db.Column(db.Integer)

    product = db.relationship('Product', backref="categories")

    def __repr__(self):
        return self.name
