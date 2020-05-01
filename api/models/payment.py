from . import db
from .abc import BaseModel
from sqlalchemy.sql import func


class PaymentLog(db.Model, BaseModel):
    __tablename__ = 'payment_logs'

    id = db.Column(db.Integer(), primary_key=True)
    msisdn = db.Column(db.String(15), nullable=False)
    subscriber_id = db.Column(db.Integer, db.ForeignKey('subscribers.id'), nullable=True)
    amount = db.Column(db.Integer)  # measured in kobo
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('product_categories.id'))
    payment_mode = db.Column(db.String(50), nullable=False)
    txn_reference = db.Column(db.String(50), nullable=True)
    status = db.Column(db.String(50), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())

    product = db.relationship('Product', backref="payments")
    category = db.relationship('ProductCategory', backref="payments")
    subscriber = db.relationship('Subscriber', backref="payments")
