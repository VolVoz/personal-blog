import functools
import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart

from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from flask import Flask, render_template, flash, redirect, request, \
    url_for, session
from flask.ext.sqlalchemy import SQLAlchemy
from flask_mailer import Mailer
from micawber import bootstrap_basic
from micawber.cache import Cache as OEmbedCache
from playhouse.sqlite_ext import *
from sqlalchemy import desc
from sqlalchemy import exc

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config.from_object('config.DevelopmentConfig')
db = SQLAlchemy(app)
oembed_providers = bootstrap_basic(OEmbedCache())
smtp = Mailer(app)

from models import *


def login_required(fn):
    @functools.wraps(fn)
    def inner(*args, **kwargs):
        if session.get('logged_in'):
            return fn(*args, **kwargs)
        return redirect(url_for('login', next=request.path))
    return inner


class Mail:
    def __init__(self):
        pass

    @staticmethod
    def send_mail(message):
        gmailUser = 'myflaskvozniakblog@gmail.com'
        gmailPassword = 'Vova1994'
        recipient = 'vozniak.vol@hotmail.com'
        mailServer = smtplib.SMTP('smtp.gmail.com', 587)
        mailServer.ehlo()
        mailServer.starttls()
        mailServer.ehlo()
        mailServer.login(gmailUser, gmailPassword)
        mailServer.sendmail(gmailUser, recipient, message.as_string())
        mailServer.close()


@app.route('/')
def index():
    query = Entry.query.order_by(desc(Entry.timestamp)).all()
    return render_template('index.html', object_list=query)


@app.route('/about/')
def about():
    return render_template('about.html')


@app.route('/contact/', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        m = Mail()
        msg = MIMEMultipart()
        msg['Subject'] = "New answer from BLOG"
        message = "\nHello, my name is " + request.form['name'] + ".\n My phone: " + request.form['phone'] + ".\n My email: " + request.form['email'] + ".\n Message: " + request.form['message']
        msg.attach(MIMEText(message))
        try:
            m.send_mail(msg)
            flash('Thank you!', 'success')
        except:
            flash('Oops, some shit happends with smtp.. sorry, I fix it at next commit!', 'danger')
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
            new_entry = Entry(
                title=request.form['title'],
                content=request.form['content'],
                timestamp=datetime.utcnow().isoformat(),
                slug=re.sub('[^\w]+', '-', request.form['title'].lower()).strip('-'))
            for keyword in request.form.get("keywords").split(","):
                if keyword in [key.name for key in Keywords.query.all()]:
                    curr_key = Keywords.query.filter_by(name=keyword).first()
                    new_entry.keywords.append(curr_key)
                else:
                    new_key = Keywords(keyword)
                    Keywords.add_keyword(new_key)
                    new_entry.keywords.append(new_key)
            try:
                Entry.add_entry(new_entry)
                flash('Entry created successfully.', 'success')
                return render_template('detail.html', entry=new_entry)
            except exc.SQLAlchemyError:
                flash('Something wrong happened with db.', 'danger')
    return render_template('create.html', keywords=Keywords.query.all())


@app.route('/<slug>/edit/', methods=['GET', 'POST'])
@login_required
def edit(slug):
    if Entry.query.filter_by(slug=slug).first():
        entry = Entry.query.filter_by(slug=slug).first()
        if request.method == 'POST' and request.form.get('_method', '').upper() == 'DELETE':
            try:
                Entry.delete_entry(entry)
                flash('Entry deleted successfully.', 'success')
                return render_template('index.html')
            except exc.SQLAlchemyError:
                flash('Cant delete row, SQLAlchemy pizdec!', 'danger')
        elif request.method == 'POST' and request.form.get('_method', '').upper() == 'EDIT':
            if request.form.get('title') and request.form.get('content'):
                entry.title = request.form.get('title')
                entry.content = request.form.get('content')
                try:
                    db.session.commit()
                    flash('Entry updated successfully.', 'success')
                    return render_template('detail.html', entry=entry)
                except exc.SQLAlchemyError:
                    flash('Something wrong happened with edit entry.', 'danger')
            else:
                flash('Title and Content are required,dude!', 'danger')
        return render_template('edit.html', entry=entry, keywords=Keywords.query.all())
    return render_template('404.html')


@app.route('/<slug>/')
def detail(slug):
    if Entry.query.filter_by(slug=slug).first():
        entry = Entry.query.filter_by(slug=slug).first()
        return render_template('detail.html', entry=entry)
    return render_template('404.html')


@app.route('/sort_by/<keyword>/')
def sort_by(keyword):
    query = Entry.query.order_by(desc(Entry.timestamp)).all()
    return render_template('index.html', object_list=[e for e in query if keyword in [k.name for k in e.keywords]])


@app.errorhandler(404)
def not_found(exc):
    return render_template('404.html')

if __name__ == '__main__':
    app.run()
