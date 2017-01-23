import os
import unittest
import coverage
from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand

from app import create_app
from app.database import db

app = create_app()
app.config.from_object(os.environ['APP_SETTINGS'])
manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)
manager.add_command('start', Server(host=os.environ.get('IP', '0.0.0.0'),  # command for run app in browser IDE
                                    port=int(os.environ.get('PORT', 8080))))

@manager.command
def test():
    """Runs the unit tests without coverage."""
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


@manager.command
def cov():
    """Runs the unit tests with coverage."""
    cov = coverage.coverage(
        branch=True,
        include='app/*',
        omit=['*/__init__.py']
    )
    cov.start()
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    cov.stop()
    cov.save()
    print 'Coverage Summary:'
    cov.report()
    basedir = os.path.abspath(os.path.dirname(__file__))
    covdir = os.path.join(basedir, 'cover')
    cov.html_report(directory=covdir)
    print('HTML version: file://%s/index.html' % covdir)
    cov.erase()


@manager.command
def create_data():
    """Creates sample data."""
    pass

if __name__ == '__main__':
    manager.run()
