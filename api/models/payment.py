from . import db
from .abc import BaseModel
from sqlalchemy.sql import func
import enum


class StatusEnum(str, enum.Enum):
    Pending = "Pending"
    Paid = "Paid"
    Unpaid = "Unpaid"


class PaymentModeEnum(str, enum.Enum):
    MTN = "MTN"
    Paystack = "Paystack"


class PaymentTypeEnum(str, enum.Enum):
    SUBSCRIPTION = "SUBSCRIPTION"
    PURCHASE = "PURCHASE"


class Transaction(db.Model, BaseModel):
    __tablename__ = 'transactions'

    id = db.Column(db.Integer(), primary_key=True)
    msisdn = db.Column(db.String(15), nullable=False)
    subscriber_id = db.Column(db.Integer, db.ForeignKey('subscribers.id'), nullable=True)
    amount = db.Column(db.Integer)  # measured in kobo
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('product_categories.id'), nullable=True)
    payment_mode = db.Column(db.Enum(PaymentModeEnum))
    payment_type = db.Column(db.Enum(PaymentTypeEnum))
    txn_reference = db.Column(db.String(50), nullable=True)
    status = db.Column(db.Enum(StatusEnum), default=StatusEnum.Pending)
    note = db.Column(db.Text, nullable=True)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())

    product = db.relationship('Product', backref="transactions")
    category = db.relationship('ProductCategory', backref="transactions")
    subscriber = db.relationship('Subscriber', backref="transactions")


class TransactionItem(db.Model, BaseModel):
    __tablename__ = 'transaction_items'

    id = db.Column(db.Integer(), primary_key=True)
    transaction_id = db.Column(db.Integer, db.ForeignKey('transactions.id'))
    item = db.Column(db.String(50))

    transaction = db.relationship('Transaction', backref="items")

    def __repr__(self):
        return self.item
