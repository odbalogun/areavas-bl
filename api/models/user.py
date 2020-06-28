from . import db
from .abc import BaseModel
from flask_security import RoleMixin, UserMixin
from sqlalchemy.sql import func


roles_admin_users = db.Table(
    'roles_admin_users',
    db.Column('admin_user_id', db.Integer(), db.ForeignKey('admin_user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __str__(self):
        return self.name


class AdminUser(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean(), nullable=False)
    roles = db.relationship('Role', secondary=roles_admin_users, backref='admin_users')

    def __str__(self):
        return self.first_name + " " + self.last_name + " <" + self.email + ">"


class User(db.Model, BaseModel):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=True)
    last_name = db.Column(db.String(255), nullable=True)
    email = db.Column(db.String(255), nullable=True)
    msisdn = db.Column(db.String(15), nullable=False, unique=True)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())

    def __str__(self):
        return self.msisdn

    def __repr__(self):
        return self.msisdn

    @classmethod
    def create_or_get(cls, **kwargs):
        instance = cls.query.filter(**kwargs).first()
        if instance:
            return instance
        instance = cls(**kwargs)
        instance.save()
        return instance

    @property
    def status(self):
        if not self.subscription:
            return
        return self.subscription.status
