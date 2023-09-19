import os
from pathlib import Path

cwd = Path(__file__).parent


class BaseConfig:
    SECRET_KEY = os.urandom(24)
    WTF_CSRF_SECRET_KEY = os.urandom(24)

    DEBUG_TB_INTERCEPT_REDIRECTS = False  # Disable redirect interception

    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = "pleahmacaka@gmail.com"
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = "Support Team <pleahmacaka@gmail.com>"

    UPLOAD_FOLDER = str(Path(cwd, "images"))


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
