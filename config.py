import os


class Config(object):
    DEBUG = True
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'volvoz'
    ADMIN_PASSWORD = 'volvoz'
    SQLALCHEMY_DATABASE_URI = 'postgresql://volvoz:volvoz@localhost/volvoz-blog'
    SITE_WIDTH = 800


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://volvoz:volvoz@localhost/volvoz-blog'
