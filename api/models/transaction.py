from . import db
from .abc import BaseModel, PAYMENT_STATUS_OPTIONS, MODE_OPTIONS, TYPE_OPTIONS
from sqlalchemy.sql import func


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
        # validate transactions
        sub = int(kwargs.get('txn_type'))
        # subscription requires no user_id but requires category_id
        if sub == 0:
            if kwargs.get('user_id'):
                raise ValueError("New subscriber should not have user_id")
            if not kwargs.get('category_id'):
                raise ValueError("Subscription requires a category id")

        # renewal requires user_id & category id
        if sub == 2:
            if not kwargs.get('category_id') or not kwargs.get('user_id'):
                raise ValueError("Renewals must include category_id and user_id")

        # purchase requires items
        if sub == 1:
            if not kwargs.get('items'):
                raise ValueError("Invalid purchase request. No items provided")
        self.items = kwargs.get('items')
        self.txn_type = kwargs.get('txn_type')
        self.mode = kwargs.get('mode')
        super().__init__(**kwargs)

    @property
    def status(self):
        return PAYMENT_STATUS_OPTIONS.get(self._status)

    @status.setter
    def status(self, val):
        if val not in PAYMENT_STATUS_OPTIONS.keys():
            raise ValueError("Invalid status provided")
        self._status = val

    @property
    def identity_email(self):
        return f"{self.msisdn}{self.id}@barrillo.net"


class BillingLog(BaseTransaction):
    __tablename__ = 'billing_logs'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)
    validity = db.Column(db.Integer)

    category = db.relationship('Category', backref="billing_logs")
    user = db.relationship('User', backref="billing_logs")