from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import SubmitField


class UploadImageForm(FlaskForm):
    image = FileField(
        validators=[
            FileAllowed(["jpg", "jpeg", "png"], "Images only!"),
            FileRequired("File was empty!")
        ]
    )
    submit = SubmitField("Upload")
