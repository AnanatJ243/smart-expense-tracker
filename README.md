# Smart Expense Tracker & Budget Management System

A modular Python CLI application for tracking expenses, managing category budgets, generating analytics, exporting reports, visualizing spending, and backing up/restoring data.

## Features

- Add, update, delete, view and filter expenses
- Search expenses by description keyword
- Filters by date range, category and payment mode
- Monthly budgets per category
- Real-time budget utilization with 80% and 100% alerts
- Monthly/category-wise summaries using Pandas
- Total spending, average daily spending and highest-spend category
- CSV and PDF report export
- Pie chart: category distribution
- Line chart: daily spending trend
- Bar chart: budget vs actual
- SQLite persistence across application restarts
- JSON backup and restore
- Input validation and friendly error handling
- OOP and modular package architecture

## Technologies Used

Python 3.10+, SQLite, Pandas, Matplotlib, Seaborn and ReportLab.

## Architecture

```
smart-expense-tracker/
├── src/
│   ├── models/       # Expense and Budget domain models
│   ├── services/     # Tracking and reporting business logic
│   ├── storage/      # SQLite persistence and backup/restore
│   ├── utils/        # Validation helpers
│   └── main.py       # Menu-driven CLI
├── data/             # Runtime SQLite database and backups
├── reports/          # Generated CSV/PDF/PNG reports
├── requirements.txt
├── DEMO_SCRIPT.md
└── README.md
```

## Setup

Install Python 3.10 or newer, then:

```bash
python -m venv .venv
```

Windows:
```bash
.venv\\Scripts\\activate
```

macOS/Linux:
```bash
source .venv/bin/activate
```

Install packages:

```bash
pip install -r requirements.txt
```

Run:

```bash
python -m src.main
```

The SQLite database is automatically created as `data/expenses.db`.

## Demonstration Flow

Use `DEMO_SCRIPT.md` for the required video sequence: CRUD operations, filtering/search, budget alerts, reports, all three visualizations, restart/persistence, and backup/restore.

## Screenshots

For the coursework submission, capture screenshots while running the CLI and place them in `screenshots/`. Recommended captures are:
1. Main menu
2. Expense list after adding/updating records
3. Budget status showing an alert
4. Monthly report
5. Pie chart
6. Spending trend
7. Budget-vs-actual chart

## Error Handling

The application rejects negative/zero amounts, invalid dates, unsupported categories/payment modes, empty descriptions and invalid months. Database/file errors are caught by the CLI and displayed as user-friendly messages. Backup restoration also validates the JSON structure before replacing records.

## Data Persistence

SQLite stores expenses and budgets permanently between sessions. JSON backup contains both datasets and can restore them after accidental changes.

## Coursework Deliverables

- Complete modular source code
- README with setup and feature documentation
- DEMO_SCRIPT.md for the compulsory video
- CSV/PDF/PNG reports generated at runtime
- SQLite data persistence
