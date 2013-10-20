__author__ = 'Radu'

from flask.ext.login import current_user, login_user, LoginManager, UserMixin
from sqlalchemy.orm import mapper

from crossco import app

db = app.db

user_services = db.Table('user_services',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('service_id', db.Integer, db.ForeignKey('service.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('date_added', db.DateTime)
)

admin_services = db.Table('admin_services',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('service_id', db.Integer, db.ForeignKey('service.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('permissions', db.Unicode(256))
)

class UserServices(object):
     def __init__(self, id=None, service_id=None, user_id=None, date_added=None):
        self.id = id
        self.service_id = service_id
        self.user_id = user_id
        self.date_added = date_added

class AdminServices(object):
     def __init__(self, id=None, service_id=None, user_id=None, permissions=None):
        self.id = id
        self.service_id = service_id
        self.user_id = user_id
        self.permissions = permissions

mapper(UserServices, user_services)
mapper(AdminServices, admin_services)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    fb_id = db.Column(db.Unicode(64))
    fb_data = db.Column(db.UnicodeText)
    used_services = db.relationship('Service', secondary=user_services,
        backref=db.backref('users', lazy='dynamic'))
    admined_services = db.relationship('Service', secondary=admin_services,
        backref=db.backref('admins', lazy='dynamic'))
    #actions = db.relationship('Action')

class Action(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'))
    action = db.Column(db.Unicode(64))
    date_time = db.Column(db.DateTime)
    message =db.Column(db.Unicode(200))

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(64))
    parent_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    parent = db.relationship('Category', primaryjoin="Category.id==Category.parent_id")

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cat_id = db.Column(db.Integer)
    name = db.Column(db.Unicode(64))
    fb_category = db.Column(db.String(128))
    fb_id = db.Column(db.String(40))
    fb_access_token = db.Column(db.Text)
    #category = db.relationship('Category', primaryjoin="Service.cat_id==Category.id")
