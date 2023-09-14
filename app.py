from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect

from config import config

db = SQLAlchemy()
csrf = CSRFProtect()


def create_app(config_key: str):
    app = Flask(__name__)

    app.config.from_object(config[config_key])

    print(" * Running app as " + config_key + " mode  <--")

    # === Init Extensions ===
    csrf.init_app(app)
    db.init_app(app)

    Migrate(app, db)

    from crud import views as crud_views  # must be here to avoid circular import
    app.register_blueprint(crud_views.crud, url_prefix='/crud')

    return app
