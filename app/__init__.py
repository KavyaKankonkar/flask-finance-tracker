from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = "finance-secret-key-2024"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///finance.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    from app.routes.auth import auth_bp
    from app.routes.transactions import transactions_bp
    from app.routes.summary import summary_bp
    from app.routes.admin import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(transactions_bp)
    app.register_blueprint(summary_bp)
    app.register_blueprint(admin_bp)

    with app.app_context():
        db.create_all()
        from app.services.seed import seed_data
        seed_data()

    return app
