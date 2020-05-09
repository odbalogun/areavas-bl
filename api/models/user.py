from . import db
from flask_security import RoleMixin, UserMixin


roles_admin_users = db.Table(
    'roles_admin_users',
    db.Column('admin_user_id', db.Integer(), db.ForeignKey('admin_user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key = True)
    name = db.Column(db.String(80), unique = True)
    description = db.Column(db.String(255))

    def __str__(self):
        return self.name


class AdminUser(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique = True, nullable = False)
    password = db.Column(db.String(255), nullable = False)
    active = db.Column(db.Boolean(), nullable = False)
    roles = db.relationship('Role', secondary = roles_admin_users, backref = 'admin_users')

    def __str__(self):
        return self.first_name + " " + self.last_name + " <" + self.email + ">"