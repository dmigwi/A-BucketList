import os
import tempfile

BASEDIR = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    DATABASE = tempfile.mktemp()
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = 'confidential top secret!'
    TRAP_HTTP_EXCEPTIONS = False


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql://user@localhost/foo'


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///%sapp.db' % BASEDIR
    # DEBUG = True


class TestingConfig(Config):
    SECRET_KEY = 'the tests refactoring'
    TESTING = True
    DEBUG = True
    TRAP_HTTP_EXCEPTIONS = True
