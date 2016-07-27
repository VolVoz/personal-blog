import os
from flask import Flask
from .database import db


def create_app():
    app = Flask(__name__)
    app.config.from_object(os.environ['APP_SETTINGS'])

    db.init_app(app)
    with app.test_request_context():
        db.create_all()

    import blog.controllers as blog
    import general.controllers as general
    import entries.controllers as entries

    app.register_blueprint(general.module)
    app.register_blueprint(blog.module)
    app.register_blueprint(entries.module)

    return app
