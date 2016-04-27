from app import db, oembed_providers
from config import Config
from markdown import markdown
from markdown.extensions.codehilite import CodeHiliteExtension
from markdown.extensions.extra import ExtraExtension
from micawber import parse_html
from flask import Markup


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

    @property
    def html_content(self):
        hilite = CodeHiliteExtension(linenums=False, css_class='highlight')
        extras = ExtraExtension()
        markdown_content = markdown(self.content, extensions=[hilite, extras])
        oembed_content = parse_html(
            markdown_content,
            oembed_providers,
            urlize_all=True,
            maxwidth=Config.SITE_WIDTH)
        return Markup(oembed_content)

    def __init__(self, title, content, published, timestamp, slug):
        self.title = title
        self.content = content
        self.published = published
        self.timestamp = timestamp
        self.slug = slug

    def __repr__(self):
        return '<Entry %r>' % self.slug
