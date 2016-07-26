from flask.ext.script import Manager, Server
from flask.ext.migrate import Migrate, MigrateCommand
import os
from app import app
from database import db

app.config.from_object(os.environ['APP_SETTINGS'])
db.init_app(app)

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

# command for run app in browser IDE
manager.add_command("start", Server(host=os.environ.get('IP', '0.0.0.0'),port=int(os.environ.get('PORT', 8080))))
if __name__ == '__main__':
    manager.run()
