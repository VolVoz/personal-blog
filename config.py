import os


class Config(object):
    DEBUG = True
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ['SECRET_KEY']
    ADMIN_PASSWORD = os.environ['ADMIN_PASSWORD']
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    SITE_WIDTH = 800


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class Testing(Config):
    TESTING = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    TESTING = True
