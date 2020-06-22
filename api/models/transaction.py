from . import db
from .abc import BaseModel
from sqlalchemy.sql import func

STATUS_OPTIONS = {
    0: "pending",
    1: "paid",
    2: "failed"
}

MODE_OPTIONS = {
    0: "paystack",
    1: "mtn"
}

TYPE_OPTIONS = {
    0: "subscription",
    1: "purchase",
    2: "renewal"
}


class BaseTransaction(db.Model, BaseModel):
    __abstract__ = True

    id = db.Column(db.Integer(), primary_key=True)
    price = db.Column(db.Integer)  # measured in kobo
    _items = db.Column(db.Text, nullable=True)
    _mode = db.Column(db.Integer, default=0)
    _type = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())

    @property
    def items(self):
        return self._items

    @items.setter
    def items(self, value_list):
        if value_list:
            self._items = ", ".join(value_list)

    @property
    def mode(self):
        return MODE_OPTIONS.get(self._mode)

    @mode.setter
    def mode(self, val):
        if val not in MODE_OPTIONS.keys():
            raise ValueError("Invalid mode provided")
        self._mode = val

    @property
    def txn_type(self):
        return TYPE_OPTIONS.get(self._type)

    @txn_type.setter
    def txn_type(self, val):
        if val not in TYPE_OPTIONS.keys():
            raise ValueError("Invalid transaction type provided")
        self._type = val


class Transaction(BaseTransaction):
    __tablename__ = 'transactions'

    msisdn = db.Column(db.String(15), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)
    txn_reference = db.Column(db.String(50), nullable=True)
    _status = db.Column(db.Integer, default=0)

    category = db.relationship('Category', backref="transactions")
    user = db.relationship('User', backref="transactions")

    def __init__(self, **kwargs):
        # todo add logic to validate transactions
        super().__init__(**kwargs)

    @property
    def status(self):
        return STATUS_OPTIONS.get(self._status)

    @status.setter
    def status(self, val):
        if val not in STATUS_OPTIONS.keys():
            raise ValueError("Invalid status provided")
        self._status = val


class BillingLog(BaseTransaction):
    __tablename__ = 'billing_logs'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)
    validity = db.Column(db.Integer)

    category = db.relationship('Category', backref="billing_logs")
    user = db.relationship('User', backref="billing_logs")