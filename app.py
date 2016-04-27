from flask.ext.sqlalchemy import SQLAlchemy
from flask import Flask, render_template, flash, redirect, request, \
    url_for, session
from datetime import datetime
import functools
from sqlalchemy import desc
from playhouse.sqlite_ext import *
from sqlalchemy import exc
from micawber import bootstrap_basic
from micawber.cache import Cache as OEmbedCache

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config.from_object('config.Config')
db = SQLAlchemy(app)
oembed_providers = bootstrap_basic(OEmbedCache())

from models import *


def login_required(fn):
    @functools.wraps(fn)
    def inner(*args, **kwargs):
        if session.get('logged_in'):
            return fn(*args, **kwargs)
        return redirect(url_for('login', next=request.path))
    return inner


@app.route('/')
def index():
    query = Entry.query.order_by(desc(Entry.timestamp)).all()
    return render_template('index.html', object_list=query)


@app.route('/about/')
def about():
    return render_template('about.html')


@app.route('/contact/')
def contact():
    return render_template('contact.html')


@app.route('/login/', methods=['GET', 'POST'])
def login():
    next_url = request.args.get('next') or request.form.get('next')
    if request.method == 'POST' and request.form.get('password'):
        password = request.form.get('password')
        if password == app.config['ADMIN_PASSWORD']:
            session['logged_in'] = True
            session.permanent = True
            flash('You are now logged in.', 'success')
            return redirect(next_url or url_for('index'))
        else:
            flash('Incorrect password.', 'danger')
    return render_template('login.html', next_url=next_url)


@app.route('/logout/', methods=['GET', 'POST'])
@login_required
def logout():
    if request.method == 'POST':
        session.clear()
        return redirect(url_for('login'))
    return render_template('logout.html')


@app.route('/create/', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        if request.form.get('title') and request.form.get('content'):
            new_entry = Entry(
                title=request.form['title'],
                content=request.form['content'],
                published=request.form.get('published') or False,
                timestamp=datetime.utcnow().isoformat(),
                slug=re.sub('[^\w]+', '-', request.form['title'].lower()).strip('-'))
            print "Here"
            try:
                db.session.add(new_entry)
                db.session.commit()
                flash('Entry created successfully.', 'success')
                print "success"
            except exc.SQLAlchemyError:
                print "WRF?"
                flash('Something wrong happend with create entry.', 'danger')
        else:
            flash('Title and Content are required.', 'danger')
    return render_template('create.html')


@app.route('/<slug>/edit/', methods=['GET', 'POST', 'DELETE'])
@login_required
def edit(slug):
    if Entry.query.filter_by(slug=slug).first():
        entry = Entry.query.filter_by(slug=slug).first()
        if request.form.get('_method', '').upper() == 'DELETE':
            try:
                db.session.delete(entry)
                db.session.commit()
                flash('Entry deleted successfully.', 'success')
                return render_template('about.html')
            except exc.SQLAlchemyError:
                flash('Cant delete row, SQLAlchemy pizdec!', 'danger')
        elif request.method == 'POST':
            if request.form.get('title') and request.form.get('content'):
                entry.title = request.form.get('title')
                entry.content = request.form.get('content')
                entry.published = request.form.get('published') or False
                try:
                    db.session.commit()
                    flash('Entry updated successfully.', 'success')
                except exc.SQLAlchemyError:
                    flash('Something wrong happend with edit entry.', 'danger')
            else:
                flash('Title and Content are required,dude!', 'danger')
        return render_template('edit.html', entry=entry)
    return render_template('404.html')


@app.route('/<slug>/')
def detail(slug):
    if Entry.query.filter_by(slug=slug).first():
        entry = Entry.query.filter_by(slug=slug).first()
        return render_template('detail.html', entry=entry)
    return render_template('404.html')


@app.errorhandler(404)
def not_found(exc):
    return render_template('404.html')

if __name__ == '__main__':
    app.debug = True
    app.run()
