from . import db
from .abc import BaseModel, STATUS_OPTIONS, MODE_OPTIONS
from sqlalchemy.sql import func
from sqlalchemy.orm import backref


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

    user = db.relationship('User', backref=backref('subscription', uselist=False))

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
        print("here: "+val)
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

    user = db.relationship('User', backref='unsubscription_logs')

    @property
    def mode(self):
        return MODE_OPTIONS.get(self._mode)

    @mode.setter
    def mode(self, val):
        if val not in MODE_OPTIONS.keys():
            raise ValueError("Invalid subscription mode provided")
        self._mode = val