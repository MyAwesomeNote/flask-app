from datetime import datetime

from flask_login import UserMixin

from app import db


class UserImage(db.Model, UserMixin):
    __tablename__ = "user_images"

    def  __init__(self, user_id, image_path):
        self.user_id = user_id
        self.image_path = image_path

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String, db.ForeignKey("users.id"))
    image_path = db.Column(db.String)
    is_detected = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
