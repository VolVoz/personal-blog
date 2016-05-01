class Config(object):
    DEBUG = True
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'steve_vozniak'
    ADMIN_PASSWORD = 'volvoz'
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    SITE_WIDTH = 800


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://volvoz:volvoz@localhost/volvoz-blog'


class TestingConfig(Config):
    TESTING = True
