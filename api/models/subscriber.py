from . import db
from .abc import BaseModel
from sqlalchemy.sql import func
import enum


class StatusEnum(enum.Enum):
    active = "Active"
    expired = "Expired"
    deactivated = "Deactivated"


class SubscriptionModeEnum(enum.Enum):
    mtn = "MTN"
    paystack = "Paystack"


class Subscriber(db.Model, BaseModel):
    __tablename__ = 'subscribers'

    id = db.Column(db.Integer(), primary_key=True)
    msisdn = db.Column(db.String(15), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('product_categories.id'), nullable=False)
    initial_sub_date = db.Column(db.DateTime(timezone=True))
    last_renewed_date = db.Column(db.DateTime(timezone=True))
    expiry_date = db.Column(db.DateTime(timezone=True))
    status = db.Column(db.Enum(StatusEnum), default=StatusEnum.active)
    subscription_mode = db.Column(db.Enum(SubscriptionModeEnum))
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    date_updated = db.Column(db.DateTime(timezone=True))

    product = db.relationship('Product', backref="subscribers")
    category = db.relationship('ProductCategory', backref="subscribers")

    def __repr__(self):
        return self.msisdn