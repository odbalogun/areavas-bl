from sqlalchemy import inspect
from datetime import datetime
import time

from . import db

STATUS_OPTIONS = {
    "active": 0,
    "expired": 1
}

MODE_OPTIONS = {
    "paystack": 0,
    "mtn": 1
}

PAYMENT_STATUS_OPTIONS = {
    "pending": 0,
    "paid": 1,
    "failed": 2
}

TYPE_OPTIONS = {
    "subscription": 0,
    "purchase": 1,
    "renewal": 2
}


class BaseModel:
    print_filter = ()
    to_json_filter = ()

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, {
            column: value
            for column, value in self._to_dict().items()
            if column not in self.print_filter
        })

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    @property
    def json(self):
        return {
            column: value
            if not isinstance(value, datetime) else time.mktime(value.timetuple())
            for column, value in self._to_dict().items()
            if column not in self.to_json_filter
        }

    def _to_dict(self):
        return {
            column.key: getattr(self, column.key)
            for column in inspect(self.__class__).attrs
        }

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def to_naira(self, value):
        return value/100
