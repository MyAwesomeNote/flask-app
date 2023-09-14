from flask import Blueprint, render_template, url_for, redirect

from app import db
from crud.forms import UserForm
from crud.models.user import User

crud = Blueprint(
    "crud",
    __name__,
    template_folder="templates",
    static_folder="static",
)


@crud.route("/")
def index():
    return render_template("crud/index.html")


@crud.route("/sql")
def sql_index():
    db.session.query(User).all()
    return "Please check the console for the SQL query."


@crud.route("/register", methods=["GET", "POST"])
def register():
    form = UserForm()

    if form.validate_on_submit():
        user = User(
            name=form.name.data,
            email=form.email.data,
            password=form.password.data,
        )

        db.session.add(user)
        db.session.commit()

        return redirect(url_for("crud.users"))

    return render_template("crud/register.html", form=form)


@crud.route("/users")
def users():
    _users = User.query.all()
    return render_template("crud/index.html", users=_users)


@crud.route("/users/<id>", methods=["GET", "POST"])
def edit_user(id):
    form = UserForm()

    user = User.query.filter_by(id=id).first()

    if form.validate_on_submit():
        user.username = form.name.data
        user.email = form.email.data
        user.password = form.password.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for("crud.users"))

    return render_template("crud/edit.html", user=user, form=form)


@crud.route("/users/<id>/delete", methods=["POST"])
def delete_user(id):
    user = User.query.filter_by(id=id).first()

    db.session.delete(user)
    db.session.commit()

    return redirect(url_for("crud.users"))
