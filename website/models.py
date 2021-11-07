from datetime import datetime
from flask_login import UserMixin
from . import db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(128), unique=True, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    date_created = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow())
    links = db.relationship('Link', backref='user', passive_deletes=True)

class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    title = db.Column(db.String(128), nullable=False)
    url = db.Column(db.String(512), nullable=False)
    shorten_url = db.Column(db.String(256), nullable=False)
    status = db.Column(db.String(10), nullable=False, default='public')
    date_created = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow())