from app.models.models import Transaction
from sqlalchemy import func
from app import db
from datetime import datetime, date


def get_summary(user_id):
    """
    Generates a complete financial summary for a given user.
    Returns total income, total expenses, balance, category breakdown, and monthly totals.
    """
    transactions = Transaction.query.filter_by(user_id=user_id).all()

    total_income = sum(t.amount for t in transactions if t.type == "income")
    total_expenses = sum(t.amount for t in transactions if t.type == "expense")
    balance = total_income - total_expenses

    # Category-wise breakdown of types of transaction for ease of analysis 
    category_breakdown = {}
    for t in transactions:
        key = f"{t.type}:{t.category}"
        category_breakdown[key] = category_breakdown.get(key, 0) + t.amount

    # Monthly totals (Upto last 6 months)
    monthly_totals = {}
    for t in transactions:
        month_key = t.date.strftime("%Y-%m")
        if month_key not in monthly_totals:
            monthly_totals[month_key] = {"income": 0, "expense": 0}
        monthly_totals[month_key][t.type] += t.amount

    # Sort months
    sorted_months = dict(sorted(monthly_totals.items(), reverse=True))

    # Recent activity (Till last 5)
    recent = sorted(transactions, key=lambda t: t.date, reverse=True)[:5]

    return {
        "total_income": round(total_income, 2),
        "total_expenses": round(total_expenses, 2),
        "balance": round(balance, 2),
        "category_breakdown": category_breakdown,
        "monthly_totals": sorted_months,
        "recent_activity": [t.to_dict() for t in recent],
        "total_transactions": len(transactions),
    }
