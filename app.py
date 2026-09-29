```python
import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    login_required,
    logout_user,
    current_user
)
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# --------------------------------------------------
# Configuration
# --------------------------------------------------

app.config["SECRET_KEY"] = os.getenv(
    "SECRET_KEY",
    "change-this-secret-key"
)

# --------------------------------------------------
# PostgreSQL Database Configuration
# --------------------------------------------------

database_url = os.getenv("DATABASE_URL")

if not database_url:
    raise RuntimeError("DATABASE_URL environment variable is not set")

# Convert old postgres:// URL to postgresql://
if database_url.startswith("postgres://"):
    database_url = database_url.replace(
        "postgres://",
        "postgresql://",
        1
    )

app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# --------------------------------------------------
# Flask Login Configuration
# --------------------------------------------------

login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message = "Please login to continue."


# --------------------------------------------------
# User Model
# --------------------------------------------------

class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(255),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    incomes = db.relationship(
        "Income",
        backref="user",
        lazy=True,
        cascade="all, delete-orphan"
    )

    expenses = db.relationship(
        "Expense",
        backref="user",
        lazy=True,
        cascade="all, delete-orphan"
    )


# --------------------------------------------------
# Income Model
# --------------------------------------------------

class Income(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    amount = db.Column(
        db.Float,
        nullable=False
    )

    source = db.Column(
        db.String(100),
        nullable=False
    )

    date = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )


# --------------------------------------------------
# Expense Model
# --------------------------------------------------

class Expense(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    amount = db.Column(
        db.Float,
        nullable=False
    )

    category = db.Column(
        db.String(100),
        nullable=False
    )

    description = db.Column(
        db.String(255)
    )

    date = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )


# --------------------------------------------------
# Login Manager
# --------------------------------------------------

@login_manager.user_loader
def load_user(user_id):

    return db.session.get(
        User,
        int(user_id)
    )


# --------------------------------------------------
# Home
# --------------------------------------------------

@app.route("/")
def home():

    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))

    return render_template("index.html")


# --------------------------------------------------
# Register
# --------------------------------------------------

@app.route("/register", methods=["GET", "POST"])
def register():

    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))

    if request.method == "POST":

        name = request.form.get("name", "").strip()

        email = request.form.get(
            "email",
            ""
        ).strip().lower()

        password = request.form.get(
            "password",
            ""
        )

        if not name or not email or not password:

            flash(
                "All fields are required.",
                "danger"
            )

            return redirect(url_for("register"))

        existing_user = User.query.filter_by(
            email=email
        ).first()

        if existing_user:

            flash(
                "Email already registered.",
                "danger"
            )

            return redirect(url_for("register"))

        hashed_password = generate_password_hash(
            password
        )

        user = User(
            name=name,
            email=email,
            password=hashed_password
        )

        db.session.add(user)
        db.session.commit()

        flash(
            "Registration successful. Please login.",
            "success"
        )

        return redirect(url_for("login"))

    return render_template("register.html")


# --------------------------------------------------
# Login
# --------------------------------------------------

@app.route("/login", methods=["GET", "POST"])
def login():

    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))

    if request.method == "POST":

        email = request.form.get(
            "email",
            ""
        ).strip().lower()

        password = request.form.get(
            "password",
            ""
        )

        user = User.query.filter_by(
            email=email
        ).first()

        if user and check_password_hash(
            user.password,
            password
        ):

            login_user(user)

            return redirect(
                url_for("dashboard")
            )

        flash(
            "Invalid email or password.",
            "danger"
        )

    return render_template("login.html")


# --------------------------------------------------
# Logout
# --------------------------------------------------

@app.route("/logout")
@login_required
def logout():

    logout_user()

    flash(
        "You have been logged out.",
        "success"
    )

    return redirect(url_for("login"))


# --------------------------------------------------
# Dashboard
# --------------------------------------------------

@app.route("/dashboard")
@login_required
def dashboard():

    incomes = Income.query.filter_by(
        user_id=current_user.id
    ).order_by(
        Income.date.desc()
    ).all()

    expenses = Expense.query.filter_by(
        user_id=current_user.id
    ).order_by(
        Expense.date.desc()
    ).all()

    total_income = sum(
        income.amount
        for income in incomes
    )

    total_expense = sum(
        expense.amount
        for expense in expenses
    )

    balance = total_income - total_expense

    return render_template(
        "dashboard.html",
        incomes=incomes,
        expenses=expenses,
        total_income=total_income,
        total_expense=total_expense,
        balance=balance
    )


# --------------------------------------------------
# Add Income
# --------------------------------------------------

@app.route("/add-income", methods=["POST"])
@login_required
def add_income():

    amount = request.form.get(
        "amount",
        type=float
    )

    source = request.form.get(
        "source",
        ""
    ).strip()

    if not amount or amount <= 0:

        flash(
            "Please enter a valid income amount.",
            "danger"
        )

        return redirect(
            url_for("dashboard")
        )

    if not source:

        flash(
            "Please enter income source.",
            "danger"
        )

        return redirect(
            url_for("dashboard")
        )

    income = Income(
        amount=amount,
        source=source,
        user_id=current_user.id
    )

    db.session.add(income)
    db.session.commit()

    flash(
        "Income added successfully.",
        "success"
    )

    return redirect(
        url_for("dashboard")
    )


# --------------------------------------------------
# Add Expense
# --------------------------------------------------

@app.route("/add-expense", methods=["POST"])
@login_required
def add_expense():

    amount = request.form.get(
        "amount",
        type=float
    )

    category = request.form.get(
        "category",
        ""
    ).strip()

    description = request.form.get(
        "description",
        ""
    ).strip()

    if not amount or amount <= 0:

        flash(
            "Please enter a valid expense amount.",
            "danger"
        )

        return redirect(
            url_for("dashboard")
        )

    if not category:

        flash(
            "Please select an expense category.",
            "danger"
        )

        return redirect(
            url_for("dashboard")
        )

    expense = Expense(
        amount=amount,
        category=category,
        description=description,
        user_id=current_user.id
    )

    db.session.add(expense)
    db.session.commit()

    flash(
        "Expense added successfully.",
        "success"
    )

    return redirect(
        url_for("dashboard")
    )


# --------------------------------------------------
# Delete Expense
# --------------------------------------------------

@app.route("/delete-expense/<int:expense_id>", methods=["POST"])
@login_required
def delete_expense(expense_id):

    expense = Expense.query.filter_by(
        id=expense_id,
        user_id=current_user.id
    ).first_or_404()

    db.session.delete(expense)
    db.session.commit()

    flash(
        "Expense deleted successfully.",
        "success"
    )

    return redirect(
        url_for("dashboard")
    )


# --------------------------------------------------
# Delete Income
# --------------------------------------------------

@app.route("/delete-income/<int:income_id>", methods=["POST"])
@login_required
def delete_income(income_id):

    income = Income.query.filter_by(
        id=income_id,
        user_id=current_user.id
    ).first_or_404()

    db.session.delete(income)
    db.session.commit()

    flash(
        "Income deleted successfully.",
        "success"
    )

    return redirect(
        url_for("dashboard")
    )


# --------------------------------------------------
# Database Initialization
# --------------------------------------------------

with app.app_context():

    db.create_all()


# --------------------------------------------------
# Vercel Entry Point
# --------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)
