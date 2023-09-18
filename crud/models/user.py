from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager


class User(db.Model, UserMixin):
    __tablename__ = "users"

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

    # column
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, index=True)
    email = db.Column(db.String, unique=True, index=True)
    password_hash = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    @property
    def password(self):
        raise AttributeError("Password is not a readable attribute.")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_duplicate_email(self):
        return User.query.filter_by(email=self.email).first() is not None


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
