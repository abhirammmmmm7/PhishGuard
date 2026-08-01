from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user
from extensions import db
from models.user import User
from models.scan import Scan
from werkzeug.security import generate_password_hash
from flask_login import current_user
from flask import Blueprint, render_template, redirect, url_for, request, flash

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/admin/dashboard")
@login_required
def admin_dashboard():

    if current_user.role != "admin":
        return "Unauthorized", 403

    # show only normal users
    users = User.query.filter(User.role != "admin").all()

    # count only normal users
    total_users = User.query.filter(User.role != "admin").count()

    total_scans = Scan.query.count()
    admins = []
    
     # ONLY super admin can see admins
    if current_user.username == "abhiram":
        admins = User.query.filter_by(role="admin").all()
    
    return render_template(
        "admin/dashboard.html",
        users=users,
        admins=admins,
        total_users=total_users,
        total_scans=total_scans,
        admin_name=current_user.username
    )
@admin_bp.route("/admin/user/<int:user_id>")
@login_required
def view_user_history(user_id):

    if current_user.role != "admin":
        return "Unauthorized", 403

    scans = Scan.query.filter_by(user_id=user_id).all()

    return render_template(
        "admin/user_history.html",
        scans=scans
    )

@admin_bp.route("/admin/delete/<int:user_id>")
@login_required
def delete_user(user_id):

    if current_user.role != "admin":
        return "Unauthorized", 403

    user = User.query.get(user_id)

    if user.role == "admin":
        return "Cannot delete admin"

    db.session.delete(user)
    db.session.commit()

    return redirect(url_for("admin.admin_dashboard"))




@admin_bp.route("/admin/create-admin", methods=["POST"])
@login_required
def create_admin():

    if current_user.username != "abhiram"  or current_user.email != "abhiram@gmail.com":
        return "Unauthorized", 403

    username = request.form["username"]
    email = request.form["email"]
    password = generate_password_hash(request.form["password"])

    # check username
    if User.query.filter_by(username=username).first():
        return redirect(url_for("admin.create_admin_page", msg="Username already exists"))

    # check email
    if User.query.filter_by(email=email).first():
        return redirect(url_for("admin.create_admin_page", msg="Email already registered"))

    admin = User(
        username=username,
        email=email,
        password_hash=password,
        role="admin"
    )

    db.session.add(admin)
    db.session.commit()

    return redirect(url_for("admin.create_admin_page", msg="Admin created successfully"))


@admin_bp.route("/admin/create-admin-page")
@login_required
def create_admin_page():

    if current_user.username != "abhiram":
        return "Unauthorized", 403

    return render_template("admin/create_admin.html")


@admin_bp.route("/admin/admins")
@login_required
def view_admins():

    if current_user.username != "abhiram":
        return "Unauthorized", 403

    admins = User.query.filter_by(role="admin").all()

    return render_template(
        "admin/admins.html",
        admins=admins,
        admin_name=current_user.username
    )
    
@admin_bp.route("/admin/delete-admin/<int:admin_id>")
@login_required
def delete_admin(admin_id):

    # only super admin
    if current_user.username != "abhiram":
        return "Unauthorized", 403

    admin = User.query.get(admin_id)

    # prevent deleting yourself
    if admin.username == "abhiram":
        return "Cannot delete super admin"

    db.session.delete(admin)
    db.session.commit()

    return redirect(url_for("admin.view_admins"))