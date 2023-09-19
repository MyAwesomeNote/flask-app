from flask_wtf import FlaskForm
from wtforms import SubmitField


class DetectorForm(FlaskForm):
    submit = SubmitField("Detect")
