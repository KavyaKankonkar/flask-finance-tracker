from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.services.summary_service import get_summary

summary_bp = Blueprint("summary", __name__)


@summary_bp.route("/summary")
@login_required
def summary():
    if current_user.role not in ("admin", "analyst"):
        from flask import flash, redirect, url_for
        flash("Access restricted. Analyst or Admin role required.", "error")
        return redirect(url_for("transactions.dashboard"))

    data = get_summary(current_user.id)
    return render_template("summary.html", data=data)
