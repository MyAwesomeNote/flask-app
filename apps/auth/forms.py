from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email


class SignUpForm(FlaskForm):
    name = StringField(
        "Username",
        validators=[
            DataRequired("Name is required"),
            Length(1, 30, "Name must be between 1 and 30 characters"),
        ]
    )
    email = StringField(
        "Email",
        validators=[
            DataRequired("Email is required"),
            Email("Email must be valid")
        ]
    )
    password = PasswordField(
        "Password",
        validators=[
            DataRequired("Password is required")
        ]
    )
    submit = SubmitField("Sign Up")


class SignInForm(FlaskForm):
    email = StringField(
        "Email",
        validators=[
            DataRequired("Email is required"),
            Email("Email must be valid")
        ]
    )
    password = PasswordField(
        "Password",
        validators=[
            DataRequired("Password is required")
        ]
    )
    submit = SubmitField("Sign In")
