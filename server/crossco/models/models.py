__author__ = 'Radu'

from flask.ext.login import current_user, login_user, LoginManager, UserMixin
# Step 3: create the user database model.
from crossco import app
db = app.db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    fb_id = db.Column(db.Unicode(64))
    fb_data = db.Column(db.UnicodeText)
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
    parent_id =db.Column(db.Integer, db.ForeignKey('category.id'))
    parent = db.relationship('Category', primaryjoin="Category.id==Category.parent_id")

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cat_id = db.Column(db.Integer)
    fb_id = db.Column(db.String(40))
    #actions = db.relationship('Action')
    #category = db.relationship('Category', primaryjoin="Service.cat_id==Category.id")


'''class Connection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    provider_id = db.Column(db.String(255))
    provider_user_id = db.Column(db.String(255))
    access_token = db.Column(db.String(255))
    secret = db.Column(db.String(255))
    display_name = db.Column(db.String(255))
    profile_url = db.Column(db.String(512))
    image_url = db.Column(db.String(512))
    rank = db.Column(db.Integer)'''
