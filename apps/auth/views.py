from flask import Blueprint, render_template, url_for, request, redirect, flash
from flask_login import login_user, logout_user

from app import db
from apps.auth.forms import SignUpForm, SignInForm
from apps.crud.models.user import User

auth = Blueprint(
    "auth",
    __name__,
    template_folder="templates",
    static_folder="static",
)


@auth.route("/")
def index():
    return render_template("auth/index.html")


@auth.route("/login")
def login():
    return redirect(url_for("auth.signin"))


@auth.route("/register")
def register():
    return redirect(url_for("auth.signup"))


@auth.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignUpForm()

    if form.validate_on_submit():
        user = User(
            name=form.name.data,
            email=form.email.data,
            password=form.password.data,
        )

        if user.is_duplicate_email():
            from flask import flash
            flash("This email is already registered", "error")
            return render_template("auth/signup.html", form=form)

        db.session.add(user)
        db.session.commit()

        login_user(user)

        next_ = request.args.get("next")
        if next_ is None or not next_.startswith("/"):
            next_ = url_for("detector.index")
            return redirect(next_)

    return render_template("auth/signup.html", form=form)


@auth.route("/signin", methods=["GET", "POST"])
def signin():
    form = SignInForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            return redirect(url_for("detector.index"))

        flash("Invalid email or password", "error")
    return render_template("auth/signin.html", form=form)


@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
