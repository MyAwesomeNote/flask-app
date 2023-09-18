from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect

from config import config

db = SQLAlchemy()
csrf = CSRFProtect()

mail = None
toolbar = None

login_manager = LoginManager()
login_manager.login_view = 'auth.signup'
login_manager.login_message = ""


def create_app(config_key: str):
    global mail, toolbar

    app = Flask(__name__)

    app.config.from_object(config[config_key])

    print(" * Running app as " + config_key + " mode  <--")

    # === Init Extensions ===
    csrf.init_app(app)
    db.init_app(app)

    login_manager.init_app(app)

    mail = Mail(app)
    toolbar = DebugToolbarExtension(app)

    Migrate(app, db)

    from apps.contact import views as contact_views
    app.register_blueprint(contact_views.contact, url_prefix='/contact')

    from apps.crud import views as crud_views
    app.register_blueprint(crud_views.crud, url_prefix='/crud')

    from apps.auth import views as auth_views
    app.register_blueprint(auth_views.auth, url_prefix='/auth')

    return app
