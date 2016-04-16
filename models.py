from app import db
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, func
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, email):
        self.email = email

    def __repr__(self):
        return '<E-mail %r>' % self.email


class Entry(db.Model):
    __tablename__ = "entries"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    slug = db.Column(db.String, unique=True)
    content = db.Column(db.String)
    published = db.Column(db.Boolean)
    timestamp = db.Column(db.DateTime)

    def __init__(self, title, content, published, timestamp, slug):
        self.title = title
        self.content = content
        self.published = published
        self.timestamp = timestamp
        self.slug = slug

    def __repr__(self):
        return '<Entry %r>' % self.slug
