import os
from pathlib import Path

cwd = Path(__file__).parent


class BaseConfig:
    SECRET_KEY = os.urandom(24)
    WTF_CSRF_SECRET_KEY = os.urandom(24)


class LocalConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + str(cwd / 'local.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True


class TestConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + str(cwd / 'test.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False


config = {
    'local': LocalConfig,
    'test': TestConfig
}
