from . import db
from .abc import BaseModel
from sqlalchemy.sql import func


STATUS_OPTIONS = {
    0: "active",
    1: "expired"
}

MODE_OPTIONS = {
    0: "paystack",
    1: "mtn"
}


class Subscription(db.Model, BaseModel):
    __tablename__ = 'subscriptions'

    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    date_updated = db.Column(db.DateTime(timezone=True), default=func.now())
    expiry_date = db.Column(db.DateTime(timezone=True))
    _status = db.Column(db.Integer, default=0)
    _mode = db.Column(db.Integer, default=0)

    @property
    def status(self):
        return STATUS_OPTIONS.get(self._status)

    @status.setter
    def status(self, val):
        if val not in STATUS_OPTIONS.keys():
            raise ValueError("Invalid status provided")
        self._status = val

    @property
    def mode(self):
        return MODE_OPTIONS.get(self._mode)

    @mode.setter
    def mode(self, val):
        if val not in MODE_OPTIONS.keys():
            raise ValueError("Invalid subscription mode provided")
        self._mode = val


class UnsubscriptionLog(db.Model, BaseModel):
    __tablename__ = 'unsubscription_logs'

    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    _mode = db.Column(db.Integer, default=0)

    @property
    def mode(self):
        return MODE_OPTIONS.get(self._mode)

    @mode.setter
    def mode(self, val):
        if val not in MODE_OPTIONS.keys():
            raise ValueError("Invalid subscription mode provided")
        self._mode = val