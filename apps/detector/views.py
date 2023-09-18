import uuid
from pathlib import Path

from flask import Blueprint, render_template, current_app, url_for, redirect
from flask_login import current_user

from app import db
from apps.crud.models.user import User
from apps.detector.forms.UploadImageForm import UploadImageForm
from apps.detector.models.user_image import UserImage

dt = Blueprint(
    "detector",
    __name__,
    template_folder="templates",
    static_folder="static",
)


@dt.route("/")
def index():
    user_images = (
        db.session.query(User, UserImage)
        .join(UserImage)
        .filter(User.id == UserImage.user_id)
        .all()
    )

    return render_template("detector/index.html", user_images=user_images)


@dt.route("/upload", methods=["GET", "POST"])
def upload_image():
    form = UploadImageForm()

    if not form.validate_on_submit():
        return render_template("detector/upload.html", form=form)

    file = form.image.data

    ext = Path(file.filename).suffix
    img_uuid_file_name = str(uuid.uuid4()) + ext
    img_path = Path(current_app.config["UPLOAD_FOLDER"], img_uuid_file_name)
    file.save(img_path)

    user_image = UserImage(
        user_id=current_user.id,
        image_path=img_path,
    )

    db.session.add(user_image)
    db.session.commit()

    return redirect(url_for("detector.index"))


@dt.route("images/<path:filename>")
def get_image(filename):
    from flask import send_from_directory
    return send_from_directory(current_app.config["UPLOAD_FOLDER"], filename)
