from database import db
from config import Config
from markdown import markdown
from markdown.extensions.codehilite import CodeHiliteExtension
from markdown.extensions.extra import ExtraExtension
from micawber import parse_html
from flask import Markup
from micawber import bootstrap_basic
from micawber.cache import Cache as OEmbedCache


oembed_providers = bootstrap_basic(OEmbedCache())
relationship_table = db.Table('relationship_table',
                              db.Column('entries_id', db.Integer, db.ForeignKey('entries.id'), nullable=False),
                              db.Column('tags_id', db.Integer, db.ForeignKey('tags.id'), nullable=False),
                              db.PrimaryKeyConstraint('entries_id', 'tags_id'))


class Entry(db.Model):
    __tablename__ = "entries"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    slug = db.Column(db.String, unique=True)
    content = db.Column(db.String)
    timestamp = db.Column(db.DateTime)
    tags = db.relationship('Tags', secondary=relationship_table, backref='entries')

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

    def __init__(self, title, content, timestamp, slug):
        self.title = title
        self.content = content
        self.timestamp = timestamp
        self.slug = slug

    @classmethod
    def add_entry(cls, entry):
        db.session.add(entry)
        return db.session.commit()

    @classmethod
    def delete_entry(cls, entry):
        db.session.delete(entry)
        return db.session.commit()

    def __repr__(self):
        return '<Entry %r>' % self.slug


class Tags(db.Model):
    __tablename__ = "tags"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)

    def __init__(self, name):
        self.name = name

    @classmethod
    def add_tag(cls, name):
        db.session.add(name)
        return db.session.commit()

    @classmethod
    def delete_tag(cls, name):
        db.session.delete(name)
        return db.session.commit()

    def __repr__(self):
        return '<Tag %r>' % self.name
