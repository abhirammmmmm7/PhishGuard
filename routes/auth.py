from flask import Blueprint, request, redirect, url_for, render_template
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user
from extensions import db
from models.user import User

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/auth", methods=["GET"])
def auth_page():
    error = request.args.get("error")
    success = request.args.get("success")
    return render_template("public/login.html", error=error, success=success)


@auth_bp.route("/auth/register", methods=["POST"])
def register():
    username = request.form["username"]
    email = request.form["email"]
    password = request.form["password"]

    existing_user = User.query.filter_by(username=username).first()

    if existing_user:
        return render_template("public/login.html", error="Username already exists")

    existing_email = User.query.filter_by(email=email).first()

    if existing_email:
        return render_template("public/login.html", error="Email already registered")

    hashed_password = generate_password_hash(password)

    user = User(
        username=username,
        email=email,
        password_hash=hashed_password,
        role="user"
    )

    db.session.add(user)
    db.session.commit()

    return redirect(url_for("auth.auth_page", success="Account created successfully. Please login."))

@auth_bp.route("/auth/login", methods=["POST"])
def login():
    email = request.form["email"]
    password = request.form["password"]

    user = User.query.filter_by(email=email).first()

    if not user:
        return render_template("public/login.html", error="User not found")

    if not check_password_hash(user.password_hash, password):
        return render_template("public/login.html", error="Incorrect password")

    login_user(user)

    if user.role == "admin":
        return redirect(url_for("admin.admin_dashboard"))
    else:
        return redirect(url_for("user.dashboard"))

@auth_bp.route("/auth/logout")
def logout():
    logout_user()
    return redirect("/")

from flask import jsonify
from werkzeug.security import generate_password_hash


@auth_bp.route("/auth/check_email", methods=["POST"])
def check_email():

    data=request.get_json()

    email=data.get("email")

    user=User.query.filter_by(email=email).first()

    if not user:
        return jsonify({"status":"not_found"})

    return jsonify({"status":"found"})


@auth_bp.route("/auth/reset_password", methods=["POST"])
def reset_password():

    data=request.get_json()

    email=data.get("email")
    password=data.get("password")

    user=User.query.filter_by(email=email).first()

    if not user:
        return jsonify({"status":"not_found"})

    user.password_hash=generate_password_hash(password)

    db.session.commit()

    return jsonify({"status":"success"})