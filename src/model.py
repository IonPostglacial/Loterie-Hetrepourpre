from dataclasses import dataclass
from app import db


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)


class User(db.Model):
    login = db.Column(db.String(256), primary_key=True)
    password_hash = db.Column(db.String())
    first_name = db.Column(db.String(256), nullable=False)
    last_name = db.Column(db.String(256), nullable=False)


class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    description = db.Column(db.String(1024), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'),
        nullable=False)
    category = db.relationship('Category',
        backref=db.backref('tickets', lazy=True))
    owner_login = db.Column(db.Integer, db.ForeignKey('user.login'),
        nullable=True)
    owner = db.relationship('User',
        backref=db.backref('tickets', lazy=True))
