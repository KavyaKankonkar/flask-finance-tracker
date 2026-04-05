from app import db, bcrypt
from app.models.models import User, Transaction
from datetime import date


def seed_data():
    """Seeds the database with demo users and transactions if not already present."""
    if User.query.first():
        return  

    # Created users for time-being demo use
    admin = User(
        username="admin",
        email="admin@finance.com",
        password=bcrypt.generate_password_hash("admin123").decode("utf-8"),
        role="admin"
    )
    analyst = User(
        username="analyst",
        email="analyst@finance.com",
        password=bcrypt.generate_password_hash("analyst123").decode("utf-8"),
        role="analyst"
    )
    viewer = User(
        username="viewer",
        email="viewer@finance.com",
        password=bcrypt.generate_password_hash("viewer123").decode("utf-8"),
        role="viewer"
    )

    db.session.add_all([admin, analyst, viewer])
    db.session.commit()

    # Sample transactions created for demo admin portal view
    sample_transactions = [
        Transaction(amount=5000, type="income", category="Salary", date=date(2024, 5, 1), notes="May salary", user_id=admin.id),
        Transaction(amount=1200, type="expense", category="Rent", date=date(2024, 5, 3), notes="Monthly rent", user_id=admin.id),
        Transaction(amount=300, type="expense", category="Groceries", date=date(2024, 5, 10), notes="Weekly groceries", user_id=admin.id),
        Transaction(amount=800, type="income", category="Freelance", date=date(2024, 5, 15), notes="Web design project", user_id=admin.id),
        Transaction(amount=150, type="expense", category="Utilities", date=date(2024, 5, 20), notes="Electricity bill", user_id=admin.id),
        Transaction(amount=5000, type="income", category="Salary", date=date(2024, 6, 1), notes="June salary", user_id=admin.id),
        Transaction(amount=1200, type="expense", category="Rent", date=date(2024, 6, 3), notes="Monthly rent", user_id=admin.id),
        Transaction(amount=500, type="expense", category="Shopping", date=date(2024, 6, 12), notes="Clothes", user_id=admin.id),
        Transaction(amount=200, type="income", category="Interest", date=date(2024, 6, 20), notes="Bank interest", user_id=admin.id),
        Transaction(amount=400, type="expense", category="Dining", date=date(2024, 6, 25), notes="Restaurants", user_id=admin.id),
    ]

    db.session.add_all(sample_transactions)
    db.session.commit()
    print("✅ Demo data seeded. Login: admin/admin123, analyst/analyst123, viewer/viewer123")
