import os
from flask.ext.sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, flash, redirect, request, \
    url_for, session, Response
from datetime import datetime
import functools


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)

import models


def login_required(fn):
    @functools.wraps(fn)
    def inner(*args, **kwargs):
        if session.get('logged_in'):
            return fn(*args, **kwargs)
        return redirect(url_for('login', next=request.path))
    return inner


@app.route('/')
def index():
    # PEACE FOR SEARCH ENTRIES
    # search_query = request.args.get('q')
    # if search_query:
    #     query = Entry.search(search_query)
    # else:
    #     query = Entry.public().order_by(Entry.timestamp.desc())
    # return object_list(
    #     'index.html',
    #     query,
    #     search=search_query,
    #     check_bounds=False)
    return render_template('index.html')


@app.route('/post')
def post():
    return render_template('post.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/login', methods=['GET', 'POST'])
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


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    if request.method == 'POST':
        session.clear()
        return redirect(url_for('login'))
    return render_template('logout.html')


@app.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        published = request.form.get('published') or False
        req = models.Entry(
            title=title,
            content=content,
            published=published,
            timestamp=datetime.utcnow().isoformat())
        db.session.add(req)
        db.session.commit()
        flash('Entry created successfully.', 'success')
    return render_template('create.html')


@app.errorhandler(404)
def not_found(exc):
    return render_template('404.html')

if __name__ == '__main__':
    app.debug = True
    app.run()
