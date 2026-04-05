from app import db
from app.models.models import Transaction
from datetime import datetime


def validate_transaction_data(data):
    """Validates incoming transaction data. Returns (cleaned_data, error_message)."""
    errors = []

    # Amount validation
    try:
        amount = float(data.get("amount", 0))
        if amount <= 0:
            errors.append("Amount must be a positive number.")
    except (ValueError, TypeError):
        errors.append("Amount must be a valid number.")
        amount = None

    # Type validation
    t_type = data.get("type", "").strip().lower()
    if t_type not in ("income", "expense"):
        errors.append("Type must be 'income' or 'expense'.")

    # Category validation
    category = data.get("category", "").strip()
    if not category:
        errors.append("Category is required.")

    # Date validation
    date_str = data.get("date", "")
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        errors.append("Date must be in YYYY-MM-DD format.")
        date = None

    notes = data.get("notes", "").strip()

    if errors:
        return None, " | ".join(errors)

    return {
        "amount": amount,
        "type": t_type,
        "category": category,
        "date": date,
        "notes": notes,
    }, None


def create_transaction(user_id, data):
    cleaned, error = validate_transaction_data(data)
    if error:
        return None, error

    txn = Transaction(
        amount=cleaned["amount"],
        type=cleaned["type"],
        category=cleaned["category"],
        date=cleaned["date"],
        notes=cleaned["notes"],
        user_id=user_id,
    )
    db.session.add(txn)
    db.session.commit()
    return txn, None


def update_transaction(txn, data):
    cleaned, error = validate_transaction_data(data)
    if error:
        return None, error

    txn.amount = cleaned["amount"]
    txn.type = cleaned["type"]
    txn.category = cleaned["category"]
    txn.date = cleaned["date"]
    txn.notes = cleaned["notes"]
    db.session.commit()
    return txn, None


def delete_transaction(txn):
    db.session.delete(txn)
    db.session.commit()


def get_filtered_transactions(user, t_type=None, category=None, start_date=None, end_date=None):
    query = Transaction.query.filter_by(user_id=user.id)

    # Filtering (available only to analyst and admin roles)
    if user.role in ("analyst", "admin"):
        if t_type:
            query = query.filter(Transaction.type == t_type)
        if category:
            query = query.filter(Transaction.category == category)
        if start_date:
            try:
                sd = datetime.strptime(start_date, "%Y-%m-%d").date()
                query = query.filter(Transaction.date >= sd)
            except ValueError:
                pass
        if end_date:
            try:
                ed = datetime.strptime(end_date, "%Y-%m-%d").date()
                query = query.filter(Transaction.date <= ed)
            except ValueError:
                pass

    return query.order_by(Transaction.date.desc()).all()
