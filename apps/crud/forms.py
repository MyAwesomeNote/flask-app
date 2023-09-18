from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, Length


class UserForm(FlaskForm):
    name = StringField(
        "name",
        validators=[
            DataRequired(message="Name field is required."),
            Length(max=30, message="Name must be less than 30 characters."),
        ],
    )
    email = StringField(
        "email",
        validators=[
            DataRequired(message="Email field is required."),
            Email(message="Email is invalid."),
        ],
    )
    password = PasswordField(
        "password",
        validators=[DataRequired(message="Password field is required.")]
    )
    submit = SubmitField("Submit")
