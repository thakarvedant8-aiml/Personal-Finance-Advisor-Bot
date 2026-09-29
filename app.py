import os
from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    login_required,
    logout_user,
    current_user,
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

database_url = os.getenv("DATABASE_URL")

if not database_url:
    raise RuntimeError("DATABASE_URL environment variable is not set")

# Support old postgres:// URLs
if database_url.startswith("postgres://"):
    database_url = database_url.replace(
        "postgres://",
        "postgresql://",
        1
    )

# Use psycopg v3
if database_url.startswith("postgresql://"):
    database_url = database_url.replace(
        "postgresql://",
        "postgresql+psycopg://",
        1
    )

app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# --------------------------------------------------
# Database
# --------------------------------------------------

db = SQLAlchemy(app)

# --------------------------------------------------
# Login Manager
# --------------------------------------------------

login_manager = LoginManager(app)
login_manager.login_view = "login"


# --------------------------------------------------
# Models
# --------------------------------------------------

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(255),
        nullable=False
    )


class Income(db.Model):
    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
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
        db.Date,
        default=datetime.utcnow().date
    )


class Expense(db.Model):
    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )

    amount = db.Column(
        db.Float,
        nullable=False
    )

    category = db.Column(
        db.String(80),
        nullable=False
    )

    description = db.Column(
        db.String(255)
    )

    date = db.Column(
        db.Date,
        default=datetime.utcnow().date
    )


class Budget(db.Model):
    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )

    month = db.Column(
        db.String(7),
        nullable=False
    )

    limit_amount = db.Column(
        db.Float,
        nullable=False
    )

    savings_target = db.Column(
        db.Float,
        nullable=False,
        default=0
    )


class SavingsGoal(db.Model):
    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )

    goal_name = db.Column(
        db.String(120),
        nullable=False
    )

    target_amount = db.Column(
        db.Float,
        nullable=False
    )

    saved_amount = db.Column(
        db.Float,
        nullable=False,
        default=0
    )


# --------------------------------------------------
# User Loader
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

    return redirect(url_for("login"))


# --------------------------------------------------
# Register
# --------------------------------------------------

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"].strip()
        email = request.form["email"].strip().lower()
        password = request.form["password"]

        existing_user = User.query.filter_by(
            email=email
        ).first()

        if existing_user:
            flash(
                "Email already registered.",
                "danger"
            )

            return redirect(
                url_for("register")
            )

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

        return redirect(
            url_for("login")
        )

    return render_template(
        "register.html"
    )


# --------------------------------------------------
# Login
# --------------------------------------------------

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"].strip().lower()
        password = request.form["password"]

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

    return render_template(
        "login.html"
    )


# --------------------------------------------------
# Logout
# --------------------------------------------------

@app.route("/logout")
@login_required
def logout():

    logout_user()

    return redirect(
        url_for("login")
    )


# --------------------------------------------------
# Dashboard
# --------------------------------------------------

@app.route("/dashboard")
@login_required
def dashboard():

    incomes = Income.query.filter_by(
        user_id=current_user.id
    ).all()

    expenses = Expense.query.filter_by(
        user_id=current_user.id
    ).all()

    total_income = sum(
        x.amount for x in incomes
    )

    total_expense = sum(
        x.amount for x in expenses
    )

    savings = total_income - total_expense

    categories = {}

    for expense in expenses:

        categories[expense.category] = (
            categories.get(
                expense.category,
                0
            ) + expense.amount
        )

    return render_template(
        "dashboard.html",
        total_income=total_income,
        total_expense=total_expense,
        savings=savings,
        categories=categories
    )


# --------------------------------------------------
# Income
# --------------------------------------------------

@app.route("/income", methods=["GET", "POST"])
@login_required
def income():

    if request.method == "POST":

        item = Income(
            user_id=current_user.id,
            amount=float(
                request.form["amount"]
            ),
            source=request.form["source"],
            date=datetime.strptime(
                request.form["date"],
                "%Y-%m-%d"
            ).date()
        )

        db.session.add(item)
        db.session.commit()

        flash(
            "Income added.",
            "success"
        )

        return redirect(
            url_for("income")
        )

    items = Income.query.filter_by(
        user_id=current_user.id
    ).order_by(
        Income.date.desc()
    ).all()

    return render_template(
        "income.html",
        items=items
    )


# --------------------------------------------------
# Expenses
# --------------------------------------------------

@app.route("/expenses", methods=["GET", "POST"])
@login_required
def expenses():

    if request.method == "POST":

        item = Expense(
            user_id=current_user.id,
            amount=float(
                request.form["amount"]
            ),
            category=request.form["category"],
            description=request.form.get(
                "description",
                ""
            ),
            date=datetime.strptime(
                request.form["date"],
                "%Y-%m-%d"
            ).date()
        )

        db.session.add(item)
        db.session.commit()

        flash(
            "Expense added.",
            "success"
        )

        return redirect(
            url_for("expenses")
        )

    items = Expense.query.filter_by(
        user_id=current_user.id
    ).order_by(
        Expense.date.desc()
    ).all()

    return render_template(
        "expenses.html",
        items=items
    )


# --------------------------------------------------
# Budget
# --------------------------------------------------

@app.route("/budget", methods=["GET", "POST"])
@login_required
def budget():

    if request.method == "POST":

        item = Budget(
            user_id=current_user.id,
            month=request.form["month"],
            limit_amount=float(
                request.form["limit_amount"]
            ),
            savings_target=float(
                request.form["savings_target"]
            )
        )

        db.session.add(item)
        db.session.commit()

        flash(
            "Budget saved.",
            "success"
        )

    items = Budget.query.filter_by(
        user_id=current_user.id
    ).order_by(
        Budget.month.desc()
    ).all()

    return render_template(
        "budget.html",
        items=items
    )


# --------------------------------------------------
# Savings
# --------------------------------------------------

@app.route("/savings", methods=["GET", "POST"])
@login_required
def savings():

    if request.method == "POST":

        item = SavingsGoal(
            user_id=current_user.id,
            goal_name=request.form["goal_name"],
            target_amount=float(
                request.form["target_amount"]
            ),
            saved_amount=float(
                request.form.get(
                    "saved_amount",
                    0
                )
            )
        )

        db.session.add(item)
        db.session.commit()

        flash(
            "Savings goal added.",
            "success"
        )

    items = SavingsGoal.query.filter_by(
        user_id=current_user.id
    ).all()

    return render_template(
        "savings.html",
        items=items
    )


# --------------------------------------------------
# Report
# --------------------------------------------------

@app.route("/report")
@login_required
def report():

    incomes = Income.query.filter_by(
        user_id=current_user.id
    ).all()

    expenses = Expense.query.filter_by(
        user_id=current_user.id
    ).all()

    total_income = sum(
        x.amount for x in incomes
    )

    total_expense = sum(
        x.amount for x in expenses
    )

    savings = (
        total_income -
        total_expense
    )

    return render_template(
        "report.html",
        total_income=total_income,
        total_expense=total_expense,
        savings=savings,
        expenses=expenses
    )


# --------------------------------------------------
# AI Financial Advice
# --------------------------------------------------

@app.route(
    "/api/ai-advice",
    methods=["POST"]
)
@login_required
def ai_advice():

    from services.gemini_service import (
        get_financial_advice
    )

    incomes = Income.query.filter_by(
        user_id=current_user.id
    ).all()

    expenses = Expense.query.filter_by(
        user_id=current_user.id
    ).all()

    total_income = sum(
        x.amount for x in incomes
    )

    total_expense = sum(
        x.amount for x in expenses
    )

    categories = {}

    for expense in expenses:

        categories[expense.category] = (
            categories.get(
                expense.category,
                0
            ) + expense.amount
        )

    advice = get_financial_advice(
        total_income,
        total_expense,
        categories
    )

    return jsonify({
        "advice": advice
    })


# --------------------------------------------------
# Create Database Tables
# --------------------------------------------------

with app.app_context():
    db.create_all()


# --------------------------------------------------
# Local Development
# --------------------------------------------------

if __name__ == "__main__":
    app.run(
        debug=True
    )
