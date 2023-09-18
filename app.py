from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect

from config import config

db = SQLAlchemy()
csrf = CSRFProtect()

mail = None
toolbar = None


def create_app(config_key: str):
    global mail, toolbar

    app = Flask(__name__)

    app.config.from_object(config[config_key])

    print(" * Running app as " + config_key + " mode  <--")

    # === Init Extensions ===
    csrf.init_app(app)
    db.init_app(app)

    mail = Mail(app)
    toolbar = DebugToolbarExtension(app)

    Migrate(app, db)

    from contact import views as contact_views
    app.register_blueprint(contact_views.contact, url_prefix='/contact')

    from crud import views as crud_views  # must be here to avoid circular import
    app.register_blueprint(crud_views.crud, url_prefix='/crud')

    return app
