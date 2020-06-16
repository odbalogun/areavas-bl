from . import db
from .abc import BaseModel
from sqlalchemy.sql import func
from sqlalchemy_utils import ChoiceType
import enum


class StatusEnum(enum.Enum):
    pending = "Pending"
    paid = "Paid"


class PaymentModeEnum(enum.Enum):
    mtn = "MTN"
    paystack = "Paystack"


class PaymentTypeEnum(enum.Enum):
    subscription = "SUBSCRIPTION"
    purchase = "PURCHASE"


class Transaction(db.Model, BaseModel):
    __tablename__ = 'transactions'

    id = db.Column(db.Integer(), primary_key=True)
    msisdn = db.Column(db.String(15), nullable=False)
    subscriber_id = db.Column(db.Integer, db.ForeignKey('subscribers.id'), nullable=True)
    amount = db.Column(db.Integer)  # measured in kobo
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('product_categories.id'), nullable=True)
    payment_mode = db.Column(ChoiceType(PaymentModeEnum))
    payment_type = db.Column(ChoiceType(PaymentTypeEnum))
    txn_reference = db.Column(db.String(50), nullable=True)
    status = db.Column(ChoiceType(StatusEnum), default=StatusEnum.pending)
    note = db.Column(db.Text, nullable=True)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())

    product = db.relationship('Product', backref="transactions")
    category = db.relationship('ProductCategory', backref="transactions")
    subscriber = db.relationship('Subscriber', backref="transactions")

    @property
    def identity_email(self):
        """
        Returns an auto-generated email address to serve as a unique identifier with Paystack
        """
        return f"{self.msisdn}@payments.barillo.net"


class TransactionItem(db.Model, BaseModel):
    __tablename__ = 'transaction_items'

    id = db.Column(db.Integer(), primary_key=True)
    transaction_id = db.Column(db.Integer, db.ForeignKey('transactions.id'))
    item = db.Column(db.String(50))

    transaction = db.relationship('Transaction', backref="items")

    def __repr__(self):
        return self.item
