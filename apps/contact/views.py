import os

from email_validator import validate_email, EmailNotValidError
from flask import Blueprint
from flask import render_template, request, flash, url_for, redirect
from flask_mail import Message

from app import mail

contact = Blueprint(
    "contact",
    __name__,
    template_folder="templates",
    static_folder="static",
)


@contact.route("/")
def index():
    return render_template("contact/hello.html")


@contact.route("/", methods=["GET"], endpoint="hello-default-ep")
def root():
    return render_template("contact/hello.html", name="Anon")


@contact.route("/<string:name>", methods=["GET"], endpoint="hello-ep")
def user(name: str):
    return render_template("contact/hello.html", name=name)


@contact.route("/us")
def us():
    return render_template("contact/us.html")


@contact.route("/complete", methods=["GET", "POST"])
def complete():
    if request.method != "POST":
        return redirect(url_for("contact.complete"))

    name = request.form.get("name")
    email = request.form.get("email")
    message = request.form.get("message")

    is_valid = True
    field_of_error = None

    if not name or not message:
        is_valid = False
        field_of_error = "name" if not name else "email" if not email else "message"
        flash(f"Please fill the {field_of_error} field", "error")

    try:
        validate_email(email)
    except EmailNotValidError:
        is_valid = False
        field_of_error = "email"

    if not is_valid:
        flash(f"Please enter a valid {field_of_error}", "error")
        return redirect(url_for("contact.us"))

    send_email(
        email,
        "Thank you for contacting us!",
        "contact_email",
        name=name,
        message=message
    )

    flash("You are already sent message once over!", "success")
    return render_template("contact/complete.html")


# noinspection PyUnresolvedReferences
def send_email(to, subject, template, **kwargs):
    msg = Message(subject, recipients=[to])

    # template file is exists?
    the_file = f"./templates/contact/emails/{template}"
    if not os.path.exists(f"{the_file}.txt") or not os.path.exists(f"{the_file}.html"):
        raise FileNotFoundError(f"Template file not found: {template}")

    msg.body = render_template(f"contact/emails/{template}.txt", **kwargs)
    msg.html = render_template(f"contact/emails/{template}.html", **kwargs)
    mail.send(msg)
