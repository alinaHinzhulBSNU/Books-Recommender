from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from app import db

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tag = db.Column(db.String(255), unique=True, nullable=False)
    #themes = db.relationship('Theme', backref='parent', cascade='all, delete-orphan')

class Publisher(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    publisher_name = db.Column(db.String(255), unique=True, nullable=False)
    #items = db.relationship('Item', backref='parent', cascade='all, delete-orphan')

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    person_name = db.Column(db.String(255), unique=True, nullable=False)
    #books = db.relationship('Book', backref='parent', cascade='all, delete-orphan')
    #roles = db.relationship('Team', backref='parent', cascade='all, delete-orphan')

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    book_title = db.Column(db.String(255), unique=True)
    original_book_title = db.Column(db.String(255), unique=True)
    age_limit = db.Column(db.String(255), default="для всіх", nullable=False)
    is_for_school = db.Column(db.Boolean, default=False)
    language = db.Column(db.String(255), default="українська", nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('person.id', ondelete='CASCADE'), nullable=False)
    description = db.Column(db.String(2000), nullable=False)
    image_url = db.Column(db.String(255), nullable=False)
    #author = db.relationship('Person', backref='books')
    #items = db.relationship('Item', backref='parent', cascade='all, delete-orphan')
    #themes = db.relationship('Theme', backref='parent', cascade='all, delete-orphan')

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id', ondelete='CASCADE'), nullable=False)
    publisher_id = db.Column(db.Integer, db.ForeignKey('publisher.id', ondelete='CASCADE'), nullable=False)
    isbn = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    pages = db.Column(db.Integer, nullable=True)
    size = db.Column(db.String(255), nullable=True)
    weight = db.Column(db.Integer, nullable=True)
    cover = db.Column(db.String(255), nullable=True)
    year = db.Column(db.Integer, nullable=True)
    url = db.Column(db.String(255), nullable=False)
    #publisher = db.relationship('Publisher', backref='items')
    #book = db.relationship('Book', backref='items')
    #staff = db.relationship('Team', backref='parent', cascade='all, delete-orphan')
    #actions = db.relationship('Action', backref='parent', cascade='all, delete-orphan')

class Theme(db.Model):
    book_id = db.Column(db.Integer, db.ForeignKey('book.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    #book = db.relationship('Book', backref='themes')
    #tag = db.relationship('Tag', backref='themes')

class Team(db.Model):
    item_id = db.Column(db.Integer, db.ForeignKey('item.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    role = db.Column(db.String(255), nullable=False)
    #person = db.relationship('Person', backref='roles')
    #item = db.relationship('Item', backref='staff')

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    gender = db.Column(db.String(255), nullable=False)
    birth_date = db.Column(db.DateTime, default=datetime.utcnow)
    #actions = db.relationship('Action', backref='parent', cascade='all, delete-orphan')

class Action(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    type = db.Column(db.String(255), nullable=False)
    #user = db.relationship('User', backref='actions')
    #item = db.relationship('User', backref='actions')
