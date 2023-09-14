import os
from pathlib import Path

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect

db = SQLAlchemy()
csrf = CSRFProtect()


def create_app():
    app = Flask(__name__)

    top_secrit = os.urandom(24)
    app.config.from_mapping(
        SECRET_KEY=top_secrit,
        SQLALCHEMY_DATABASE_URI=f"sqlite:///{Path(__file__).parent / 'db.sqlite'}",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SQLALCHEMY_ECHO=True,
        WTF_CSRF_SECRET_KEY=top_secrit,
    )

    # === Init Extensions ===
    csrf.init_app(app)
    db.init_app(app)

    Migrate(app, db)

    from crud import views as crud_views  # must be here to avoid circular import
    app.register_blueprint(crud_views.crud, url_prefix='/crud')

    return app
