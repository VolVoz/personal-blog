import re
from flask import (
    Blueprint,
    render_template,
    request,
    flash,
    abort,
)
from .models import Entry, Tags
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import desc
from datetime import datetime
from app.general.controllers import login_required, log_error


module = Blueprint('blog_entries', __name__, url_prefix='/entries')


@module.route('/create/', methods=['GET', 'POST'])
@login_required
def create():
    try:
        if request.method == 'POST':
            new_entry = Entry(title=request.form['title'],
                            content=request.form['content'],
                            timestamp=datetime.utcnow().isoformat(),
                            slug=re.sub('[^\w]+', '-', request.form['title'].lower()).strip('-'))
            for tag in request.form.get("tags").split(","):
                if len(tag.strip()) == 0:
                    continue
                elif tag in [key.name for key in Tags.query.all()]:
                    curr_key = Tags.query.filter_by(name=tag).first()
                    new_entry.tags.append(curr_key)
                else:
                    new_key = Tags(tag)
                    Tags.add_tag(new_key)
                    new_entry.tags.append(new_key)
            Entry.add_entry(new_entry)
            flash('Entry created successfully.', 'success')
            return render_template('entries/detail.html', entry=new_entry)
    except SQLAlchemyError as e:
        log_error('There was error while querying database', exc_info=e)
        flash('There was error while querying database', 'danger')
    return render_template('entries/create.html', tags=Tags.query.all())


@module.route('/<slug>/edit/', methods=['GET', 'POST'])
@login_required
def edit(slug):
    try:
        entry = Entry.query.filter_by(slug=slug).first()
        if request.method == 'POST' and request.form.get('_method', '').upper() == 'DELETE':
            Entry.delete_entry(entry)
            flash('Entry deleted successfully.', 'success')
            return render_template('blog/index.html')
        elif request.method == 'POST' and request.form.get('_method', '').upper() == 'EDIT':
            if request.form.get('title') and request.form.get('content'):
                entry.title = request.form.get('title')
                entry.content = request.form.get('content')
                Entry.update_entry()
                flash('Entry updated successfully.', 'success')
                return render_template('entries/detail.html', entry=entry)
            else:
                flash('Title and Content are required', 'danger')
    except SQLAlchemyError as e:
        log_error('Uncaught exception while querying database at entity.update', exc_info=e)
        flash('Uncaught error while querying database', 'danger')
        abort(500)
    return render_template('entries/edit.html', entry=entry, tags=Tags.query.all())


@module.route('/<slug>/')
def detail(slug):
    try:
        entry = Entry.query.filter_by(slug=slug).first_or_404()
        return render_template('entries/detail.html', entry=entry)
    except SQLAlchemyError as e:
        log_error('Entry not found', exc_info=e)
        flash('Entry not found', 'danger')
        abort(404)


@module.route('/sort_by/<tag>/')
def sort_by(tag):
    try:
        query = Entry.query.order_by(desc(Entry.timestamp)).all()
        return render_template('blog/index.html', object_list=[e for e in query if tag in [k.name for k in e.tags]])
    except SQLAlchemyError as e:
        log_error('There was error while querying database', exc_info=e)
        flash('There was error while querying database', 'danger')
        abort(500)
