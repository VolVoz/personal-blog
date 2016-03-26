import os
from flask.ext.sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request
from datetime import datetime
import models

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)


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


@app.route('/create', methods=['POST'])
def new():
    if request.method == 'POST':
        title = request.form['title']
        req = models.Entry(
            title=title,
            content="AAAAAA",
            published=True,
            timestamp=datetime.utcnow().isoformat())
        db.session.add(req)
        db.session.commit()
        return render_template('success.html')
    return render_template('create.html')

if __name__ == '__main__':
    app.debug = False
    app.run()
