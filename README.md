# Flask Finance Tracker

A backend finance tracking system built with Flask and SQLite. I built this as part of a backend development assessment. The goal was to create a system where users can manage income and expense records, view financial summaries, and have different levels of access depending on their role.

---

## What it does

- Add, view, edit and delete financial transactions (income/expense)
- Filter transactions by type, category, and date range
- Analytics page showing total income, expenses, balance, category breakdown and monthly totals
- Three user roles — admin, analyst, and viewer — each with different permissions
- Basic authentication with hashed passwords
- Input validation with proper error messages

---

## Tech Stack

- **Python / Flask** — backend framework
- **SQLite** — database (via SQLAlchemy ORM)
- **Flask-Login** — session based authentication
- **Flask-Bcrypt** — password hashing
- **Jinja2** — server side HTML templates

---

## Project Structure

```
finance_system/
├── run.py
├── requirements.txt
└── app/
    ├── __init__.py
    ├── models/
    │   └── models.py          # User and Transaction models
    ├── routes/
    │   ├── auth.py            # Login, register, logout
    │   ├── transactions.py    # CRUD + filtering
    │   ├── summary.py         # Analytics
    │   └── admin.py           # User management
    ├── services/
    │   ├── transaction_service.py   # Validation + business logic
    │   ├── summary_service.py       # Analytics calculations
    │   └── seed.py                  # Demo data
    └── templates/             # HTML pages
```

I kept routes, services, and models in separate layers so the code stays clean and each file has one clear responsibility.

---

## How to Run

```bash
# Clone the repo
git clone https://github.com/YOURUSERNAME/flask-finance-tracker.git
cd flask-finance-tracker/finance_system

# Install dependencies
pip install -r requirements.txt

# Run the app
python run.py
```

Then open **http://127.0.0.1:5000** in your browser.

> If you're on Windows and the server stops immediately, run this instead:
> `python -c "from app import create_app; app = create_app(); app.run(debug=False, use_reloader=False)"`

---

## Demo Accounts

The app automatically creates these accounts on first run:

| Username | Password    | Role     | Access |
|----------|-------------|----------|--------|
| admin    | admin123    | Admin    | Full access — CRUD, analytics, user management |
| analyst  | analyst123  | Analyst  | Add, edit, filter, analytics — no delete or user management |
| viewer   | viewer123   | Viewer   | Read only |

---

## User Roles Explained

**Admin** — complete control. Can create, edit, delete transactions and manage other users and their roles.

**Analyst** — working level access. Can add and edit transactions, use filters, and view the analytics dashboard. Cannot delete or manage users.

**Viewer** — read only. Can see the transaction list but cannot make any changes.

Role checks happen in the routes — if someone tries to access a restricted page directly via URL, they get redirected with an error message.

---

## Assumptions I Made

- Each transaction belongs to one user, no shared ledgers between users
- Filtering is available only to analyst and admin roles by design
- Admin cannot delete or change their own role (to prevent accidental lockout)
- SQLite is used to keep setup simple — switching to PostgreSQL only requires changing one config line in `app/__init__.py`

---

## What I Would Improve With More Time

- Add pagination to the transaction list for large datasets
- Write unit tests for the service layer using pytest
- Add CSV export so users can download their transaction history
- Move to a REST API structure with a proper frontend

---

## Notes

This was my first time structuring a Flask project with proper separation between routes, services, and models. Previously I used to put everything in one file. The biggest thing I learned here was keeping business logic out of the routes and into a dedicated services layer.
