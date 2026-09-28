# Personal Finance Advisor Bot — Project Documentation

## 1. Project Title
Personal Finance Advisor Bot

## 2. Abstract
The Personal Finance Advisor Bot is an AI-powered financial planning assistant developed to help individuals record income, track expenses, create budgets, monitor savings and receive personalized financial guidance. The system combines Flask, SQLAlchemy, SQLite, JavaScript and Gemini AI to provide a centralized digital environment for personal financial management.

## 3. Objectives
- Automate personal income and expense tracking.
- Generate structured monthly budgets.
- Identify category-wise spending patterns.
- Provide AI-powered budgeting and saving suggestions.
- Track savings goals.
- Produce monthly financial summaries.
- Provide a scalable full-stack architecture.

## 4. Functional Requirements
- Registration and login.
- Add income.
- Add categorized expenses.
- View transaction history.
- Create budgets.
- Create savings goals.
- View dashboard.
- Generate reports.
- Request AI recommendations.

## 5. Non-Functional Requirements
- Usability
- Security
- Maintainability
- Scalability
- Performance
- Reliability

## 6. Hardware Requirements
Processor: Intel Core i5 8th Gen or above / AMD Ryzen 5 equivalent.
RAM: Minimum 8 GB; recommended 16 GB.
Storage: 256 GB SSD or 500 GB HDD.
Internet: Minimum 10 Mbps; recommended 20 Mbps for cloud/AWS work.

## 7. Software Requirements
OS: Windows 10/11, macOS Monterey+, or Ubuntu 20.04+.
Browser: Chrome, Firefox or Edge.
IDE: VS Code.
Version control: Git.
Python: 3.8+.
AWS CLI: latest version for deployment activities.

## 8. Technology Stack
Frontend: HTML, CSS, Bootstrap, JavaScript, Chart.js.
Backend: Python Flask.
ORM: SQLAlchemy.
Database: SQLite.
AI: Gemini API.
Version Control: Git/GitHub.

## 9. Technical Architecture
Browser → HTML/CSS/JavaScript → Flask Routes → Service Layer → SQLAlchemy → SQLite.
AI requests: Flask → Gemini Service → Gemini API → AI recommendation → Dashboard.

## 10. Database Tables
User:
id, name, email, password

Income:
id, user_id, amount, source, date

Expense:
id, user_id, amount, category, description, date

Budget:
id, user_id, month, limit_amount, savings_target

SavingsGoal:
id, user_id, goal_name, target_amount, saved_amount

## 11. Scenarios
### Scenario 1 — Salaried Professional
Records salary and expenses such as rent, food, transport and entertainment. The system calculates spending and savings and provides budgeting suggestions.

### Scenario 2 — College Student
Tracks a limited allowance and controls discretionary spending using category budgets and saving suggestions.

### Scenario 3 — Freelancer
Records income from multiple clients and tracks variable expenses. Budgeting can be adjusted according to changing income.

### Scenario 4 — Household Manager
Tracks shared household income and categories such as groceries, utilities, education and healthcare and reviews consolidated spending.

## 12. Epics
1. User Authentication & Profile Management
2. Income Management
3. Expense Tracking
4. Budget Planning
5. AI Financial Advisor
6. Savings & Financial Goals
7. Dashboard & Financial Reports
8. Testing, Security & Deployment

## 13. 15 Stories/Tasks
1. User registration
2. User login/logout
3. Add/manage monthly income
4. Add daily expenses
5. Categorize expenses
6. View expense history
7. Generate monthly budget
8. Detect category-wise overspending
9. Generate AI financial recommendations
10. Create savings goals
11. Track savings progress
12. Create monthly report
13. Build dashboard and charts
14. Testing and validation
15. GitHub/AWS deployment

## 14. Testing
Unit testing should cover authentication, income calculation, expense storage, budget creation and AI-service fallback.
Integration testing should verify the flow from UI to Flask routes and database.
Security testing should check password hashing, authentication and secret-key/API-key protection.

## 15. Future Scope
Predictive spending analytics, investment education, emergency fund planning, PDF reports, email notifications, advanced financial health analysis, PostgreSQL migration, cloud deployment and mobile application support.
