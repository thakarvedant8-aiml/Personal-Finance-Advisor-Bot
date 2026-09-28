# Personal Finance Advisor Bot

AI-powered personal finance planning assistant using Flask, SQLAlchemy, SQLite, JavaScript and Gemini AI.

## Features
- User registration and login
- Monthly income tracking
- Daily/weekly expense tracking
- Category-wise expense analysis
- Budget planning
- Savings goals
- Financial dashboard
- Monthly financial report
- Chart visualization
- Gemini AI budgeting/saving advice
- Git/AWS-ready project structure

## Requirements
- Python 3.8+
- VS Code
- Git
- Internet connection
- Gemini API key (optional for AI feature)

## Installation — Windows

1. Extract the ZIP.
2. Open the project folder in VS Code.
3. Open Terminal.
4. Create virtual environment:

   python -m venv venv

5. Activate it:

   venv\Scripts\activate

6. Install packages:

   pip install -r requirements.txt

7. Copy `.env.example` to `.env`.
8. Put your Gemini API key in `.env`:

   GEMINI_API_KEY=YOUR_KEY

9. Start the application:

   python app.py

10. Open:

   http://127.0.0.1:5000

## Linux/macOS

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python app.py

Then open http://127.0.0.1:5000

## First use
1. Register a new user.
2. Login.
3. Add income.
4. Add expenses.
5. Create a budget.
6. Add savings goals.
7. Open Dashboard.
8. Click Get AI Advice.

## Important
This project provides general financial education and budgeting assistance. It is not a substitute for professional financial, investment, tax or legal advice.

## GitHub

git init
git add .
git commit -m "Initial Personal Finance Advisor Bot"
git branch -M main
git remote add origin YOUR_GITHUB_REPOSITORY_URL
git push -u origin main

## Suggested future enhancements
- Predictive expense analytics
- Investment education module
- Goal-based savings prediction
- PDF report generation
- Email monthly reports
- Admin dashboard
- AWS deployment
- PostgreSQL for production
- Role-based access
- Advanced AI financial health scoring
