import os
from flask.ext.script import Manager, Server
from flask.ext.migrate import Migrate, MigrateCommand

from app import create_app
from app.database import db

app = create_app()
app.config.from_object(os.environ['APP_SETTINGS'])
manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)
manager.add_command('start', Server(host=os.environ.get('IP', '0.0.0.0'), # command for run app in browser IDE
                                    port=int(os.environ.get('PORT', 8080))))

if __name__ == '__main__':
    manager.run()
