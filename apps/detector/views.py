import random
import uuid
from pathlib import Path

import cv2
import numpy as np
import torch
import torchvision
from PIL import Image
from flask import Blueprint, render_template, current_app, url_for, redirect, flash
from flask_login import current_user, login_required
from sqlalchemy.exc import SQLAlchemyError

from app import db
from apps.crud.models.user import User
from apps.detector.forms.DetectorForm import DetectorForm
from apps.detector.forms.UploadImageForm import UploadImageForm
from apps.detector.models import UserImage
from apps.detector.models import UserImageTag

dt = Blueprint(
    "detector",
    __name__,
    template_folder="templates",
    static_folder="static",
)


@dt.route("/")
@login_required
def index():
    user_images = (
        db.session.query(User, UserImage)
        .join(UserImage)
        .filter(User.id == UserImage.user_id)
        .all()
    )

    user_image_tag_dict = {}

    for user_image in user_images:
        user_image_tags = (
            db.session.query(UserImageTag)
            .filter(UserImageTag.user_image_id == user_image.UserImage.id)
            .all()
        )

        user_image_tag_dict[user_image.UserImage.id] = user_image_tags

    detector_form = DetectorForm()

    return render_template("detector/index.html",
                           user_images=user_images,
                           user_image_tag_dict=user_image_tag_dict,
                           detector_form=detector_form)


@dt.route("/upload", methods=["GET", "POST"])
@login_required
def upload_image():
    form = UploadImageForm()

    if not form.validate_on_submit():
        return render_template("detector/upload.html", form=form)

    file = form.image.data

    ext = Path(file.filename).suffix
    image_uuid_file_name = str(uuid.uuid4()) + ext

    # if not exist upload folder, create it
    upload_folder = Path(current_app.config["UPLOAD_FOLDER"])

    if not upload_folder.exists():
        upload_folder.mkdir()

    image_path = Path(upload_folder, image_uuid_file_name)
    file.save(image_path)

    user_image = UserImage(
        user_id=current_user.id,
        image_path=image_uuid_file_name,
    )

    db.session.add(user_image)
    db.session.commit()

    return redirect(url_for("detector.index"))


@dt.route("images/<path:filename>")
@login_required
def get_image(filename):
    from flask import send_from_directory
    return send_from_directory(current_app.config["UPLOAD_FOLDER"], filename)


def make_color(labels):
    colors = [[random.randint(0, 255) for _ in range(3)] for _ in range(len(labels))]
    return random.choice(colors)


def make_line(res_img):
    return round(0.002 * min(res_img.shape[0:2])) + 1


def draw_lines(c1, c2, res_img, line, color):
    cv2.rectangle(res_img, c1, c2, color, line)
    return cv2


def draw_texts(res_img, line, c1, cv2, color, labels, label):
    display_text = f"{labels[label]}"
    font = max(line - 1, 1)
    t_size = cv2.getTextSize(display_text, 0, font, thickness=line)[0]
    c2 = c1[0] + t_size[0] + 3, c1[1] - t_size[1] - 3
    cv2.rectangle(res_img, c1, c2, color, -1)
    cv2.putText(
        res_img,
        display_text,
        (c1[0], c1[1] - 2),
        0,
        line / 3,
        [225, 255, 255],
        thickness=font,
        lineType=cv2.LINE_AA,
    )
    return cv2


def exec_detect(target_image_path):
    labels = current_app.config["LABELS"]

    image = Image.open(target_image_path)

    image_tensor = torchvision.transforms.functional.to_tensor(image)

    model = torch.load(Path(current_app.root_path, "model.pt"))

    model = model.eval()

    output = model([image_tensor])[0]
    tags = []
    result_image = np.array(image.copy())

    for box, label, score in zip(output["boxes"], output["labels"], output["scores"]):
        if score > 0.5 and labels[label] not in tags:
            color = make_color(labels)
            line = make_line(result_image)

            c1 = (int(box[0]), int(box[1]))
            c2 = (int(box[2]), int(box[3]))

            cv2 = draw_lines(c1, c2, result_image, line, color)
            cv2 = draw_texts(result_image, line, c1, cv2, color, labels, label)
            tags.append(labels[label])

    detected_image_file_name = str(uuid.uuid4()) + ".jpg"

    detected_image_file_path = str(
        Path(current_app.config["UPLOAD_FOLDER"], detected_image_file_name)
    )
    cv2.imwrite(detected_image_file_path, cv2.cvtColor(result_image, cv2.COLOR_RGB2BGR))
    return tags, detected_image_file_name


def save_detected_image_tags(tags, detected_image_file_name, user_image):
    user_image.image_path = detected_image_file_name
    user_image.is_detected = True
    db.session.add(user_image)

    for tag in tags:
        user_image_tag = UserImageTag(
            user_image_id=user_image.id,
            tag=tag,
        )
        db.session.add(user_image_tag)

    db.session.commit()


@dt.route("/detect/<string:image_id>", methods=["POST"])
@login_required
def detect(image_id):
    user_image = db.session.query(UserImage).filter(UserImage.id == image_id).first()

    if user_image is None:
        flash("Image not found", "error")
        return redirect(url_for("detector.index"))

    target_image_path = Path(current_app.config["UPLOAD_FOLDER"], user_image.image_path)

    tags, detected_image_file_name = exec_detect(target_image_path)

    try:
        save_detected_image_tags(tags, detected_image_file_name, user_image)
    except SQLAlchemyError as e:
        db.session.rollback()
        current_app.logger.error(e)
        return redirect(url_for("detector.index"))

    return redirect(url_for("detector.index"))
