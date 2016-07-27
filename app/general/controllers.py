from flask import (
    Blueprint,
    render_template,
    redirect,
    session,
    url_for,
    request,
    current_app,
)
import functools

module = Blueprint('general', __name__)


def login_required(fn):
    @functools.wraps(fn)
    def inner(*args, **kwargs):
        if session.get('logged_in'):
            return fn(*args, **kwargs)
        return redirect(url_for('blog.login', next=request.path))
    return inner


def log_error(*args, **kwargs):
    current_app.logger.error(*args, **kwargs)


@module.app_errorhandler(404)
def handle_404(err):
    log_error('Error while querying database', exc_info=err)
    return render_template('404.html'), 404


@module.app_errorhandler(500)
def handle_500(err):
    log_error('Error while querying database', exc_info=err)
    return render_template('500.html'), 500
