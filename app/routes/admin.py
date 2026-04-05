from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models.models import User

admin_bp = Blueprint("admin", __name__)


def admin_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != "admin":
            flash("Admin access required.", "error")
            return redirect(url_for("transactions.dashboard"))
        return f(*args, **kwargs)
    return decorated


@admin_bp.route("/admin/users")
@login_required
@admin_required
def manage_users():
    users = User.query.all()
    return render_template("admin_users.html", users=users)


@admin_bp.route("/admin/users/change_role/<int:user_id>", methods=["POST"])
@login_required
@admin_required
def change_role(user_id):
    user = User.query.get_or_404(user_id)
    new_role = request.form.get("role")

    if new_role not in ("viewer", "analyst", "admin"):
        flash("Invalid role.", "error")
        return redirect(url_for("admin.manage_users"))

    if user.id == current_user.id:
        flash("You cannot change your own role.", "error")
        return redirect(url_for("admin.manage_users"))

    user.role = new_role
    db.session.commit()
    flash(f"Role updated for {user.username}.", "success")
    return redirect(url_for("admin.manage_users"))


@admin_bp.route("/admin/users/delete/<int:user_id>", methods=["POST"])
@login_required
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)

    if user.id == current_user.id:
        flash("You cannot delete yourself.", "error")
        return redirect(url_for("admin.manage_users"))

    db.session.delete(user)
    db.session.commit()
    flash(f"User {user.username} deleted.", "success")
    return redirect(url_for("admin.manage_users"))
