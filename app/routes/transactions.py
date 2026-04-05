from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models.models import Transaction
from app.services.transaction_service import (
    create_transaction, update_transaction, delete_transaction, get_filtered_transactions
)
from datetime import datetime

transactions_bp = Blueprint("transactions", __name__)


@transactions_bp.route("/dashboard")
@login_required
def dashboard():
    transactions = Transaction.query.filter_by(user_id=current_user.id).order_by(Transaction.date.desc()).limit(10).all()
    return render_template("dashboard.html", transactions=transactions)


@transactions_bp.route("/transactions")
@login_required
def list_transactions():
    # Filters from query params
    t_type = request.args.get("type")
    category = request.args.get("category")
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")

    # Analysts and admins can filter; viewers see all without filter UI
    transactions = get_filtered_transactions(current_user, t_type, category, start_date, end_date)
    categories = db.session.query(Transaction.category).filter_by(user_id=current_user.id).distinct().all()
    categories = [c[0] for c in categories]

    return render_template("transactions.html", transactions=transactions, categories=categories)


@transactions_bp.route("/transactions/add", methods=["GET", "POST"])
@login_required
def add_transaction():
    if current_user.role not in ("admin", "analyst"):
        flash("You do not have permission to add transactions.", "error")
        return redirect(url_for("transactions.dashboard"))

    if request.method == "POST":
        data = {
            "amount": request.form.get("amount"),
            "type": request.form.get("type"),
            "category": request.form.get("category"),
            "date": request.form.get("date"),
            "notes": request.form.get("notes"),
        }
        result, error = create_transaction(current_user.id, data)
        if error:
            flash(error, "error")
            return render_template("add_transaction.html")
        flash("Transaction added successfully!", "success")
        return redirect(url_for("transactions.list_transactions"))

    return render_template("add_transaction.html")


@transactions_bp.route("/transactions/edit/<int:txn_id>", methods=["GET", "POST"])
@login_required
def edit_transaction(txn_id):
    if current_user.role not in ("admin", "analyst"):
        flash("You do not have permission to edit transactions.", "error")
        return redirect(url_for("transactions.dashboard"))

    txn = Transaction.query.filter_by(id=txn_id, user_id=current_user.id).first_or_404()

    if request.method == "POST":
        data = {
            "amount": request.form.get("amount"),
            "type": request.form.get("type"),
            "category": request.form.get("category"),
            "date": request.form.get("date"),
            "notes": request.form.get("notes"),
        }
        result, error = update_transaction(txn, data)
        if error:
            flash(error, "error")
            return render_template("edit_transaction.html", txn=txn)
        flash("Transaction updated!", "success")
        return redirect(url_for("transactions.list_transactions"))

    return render_template("edit_transaction.html", txn=txn)


@transactions_bp.route("/transactions/delete/<int:txn_id>", methods=["POST"])
@login_required
def delete_transaction_route(txn_id):
    if current_user.role != "admin":
        flash("Only admins can delete transactions.", "error")
        return redirect(url_for("transactions.list_transactions"))

    txn = Transaction.query.filter_by(id=txn_id, user_id=current_user.id).first_or_404()
    delete_transaction(txn)
    flash("Transaction deleted.", "success")
    return redirect(url_for("transactions.list_transactions"))
