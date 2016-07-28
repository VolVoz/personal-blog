#!/usr/bin/python

import os
import smtplib
from flask import (
    Blueprint,
    render_template,
    request,
    flash,
    abort,
    redirect,
    url_for,
    session,
)
from app.entries.models import Entry
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import desc
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.errors import MessageError
from smtplib import SMTPAuthenticationError
from app.general.controllers import login_required, log_error
from config import Config

module = Blueprint('blog', __name__)


class Mail(object):
    def __init__(self):
        pass

    @staticmethod
    def send_mail(message):
        gmail_user = os.environ['GMAIL_USER']
        gmail_password = os.environ['GMAIL_PASS']
        recipient = 'vozniak.vol@hotmail.com'
        mail_server = smtplib.SMTP('smtp.gmail.com', 587)
        mail_server.ehlo()
        mail_server.starttls()
        mail_server.ehlo()
        mail_server.login(gmail_user, gmail_password)
        mail_server.sendmail(gmail_user, recipient, message.as_string())
        mail_server.close()


@module.route('/', defaults={'page': 1}, methods=['GET', 'POST'])
@module.route('/index/', defaults={'page': 1}, methods=['GET', 'POST'])
@module.route('/index/page/<int:page>', methods=['GET', 'POST'])
def index(page=1):
    entries = None
    try:
        entries = Entry.query.order_by(desc(Entry.timestamp)).paginate(page, Config.POSTS_PER_PAGE, False)
    except SQLAlchemyError as e:
        log_error('Error while querying database', exc_info=e)
        flash('There was uncaught database query', 'danger')
        abort(500)
    return render_template('blog/index.html', object_list=entries)


@module.route('/about/', methods=['GET'])
def about():
    return render_template('blog/about.html')


@module.route('/contact/', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        m = Mail()
        msg = MIMEMultipart()
        msg['Subject'] = "New answer from BLOG"
        message = "\nHello, my name is " + request.form['name'] + ".\n My email: " + request.form['email'] + ".\n Message: " + request.form['message']
        msg.attach(MIMEText(message))
        try:
            m.send_mail(msg)
            flash('Thank you!', 'success')
        except (MessageError, SMTPAuthenticationError) as e:
            log_error('There was error while sending email', exc_info=e)
            flash('There was error while sending email', 'danger')
    return render_template('blog/contact.html')


@module.route('/login/', methods=['GET', 'POST'])
def login():
    next_url = request.args.get('next') or request.form.get('next')
    if request.method == 'POST' and request.form.get('password'):
        password = request.form.get('password')
        if password == os.environ['ADMIN_PASSWORD']:
            session['logged_in'] = True
            session.permanent = True
            flash('You are now logged in.', 'success')
            return redirect(next_url or url_for('blog.index'))
        else:
            flash('Incorrect password.', 'danger')
    return render_template('blog/login.html', next_url=next_url)


@module.route('/logout/', methods=['GET', 'POST'])
@login_required
def logout():
    if request.method == 'POST':
        session.clear()
        return redirect(url_for('blog.login'))
    return render_template('blog/logout.html')
