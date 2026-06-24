# 💰 Expense Tracker — CLI Personal Finance Manager

> A clean, beginner-to-intermediate Python portfolio project demonstrating OOP,
> file I/O, exception handling, and a polished terminal interface.

---

## 📁 Folder Structure

```
expense_tracker/
├── expense_tracker.py   # Main application (all source code)
├── expenses.csv         # Auto-created data file (sample data included)
├── expense_report.txt   # Generated when you export a report
└── README.md            # This file
```

---

## ✨ Features

| Feature | Details |
|---|---|
| Add Expense | Date, amount, category, description |
| View All | Sorted table with grand total |
| Search by Category | Filter expenses by category |
| Total Expenses | Grand total + ASCII bar chart |
| Monthly Summary | Month-by-month breakdown |
| Category Analysis | Visual percentage chart |
| Delete Expense | Remove by ID with confirmation |
| Export Report | Full `.txt` summary report |
| Budget Warnings | Alert at 80 % and 100 % of limit |
| Persistent Storage | All data saved to `expenses.csv` |

---

## 🚀 How to Run

### Prerequisites
- Python **3.8** or higher (no third-party libraries needed)

### Step 1 — Clone / download the project
```bash
git clone https://github.com/YOUR_USERNAME/expense-tracker.git
cd expense-tracker
```

### Step 2 — Run the app
```bash
python expense_tracker.py
```

On Windows you may need:
```bash
py expense_tracker.py
```

### Step 3 — Use the menu
```
  MAIN MENU
  ──────────────────────────────
  [1] Add Expense
  [2] View All Expenses
  [3] Search by Category
  [4] Show Total Expenses
  [5] Monthly Summary
  [6] Category Analysis
  [7] Delete Expense
  [8] Export Summary Report
  [9] Set Budget Limit
  [0] Exit
  ──────────────────────────────
```

---

## 🧱 Code Architecture

### `Expense` class — Data Model
```
Expense
 ├── expense_id  : int
 ├── date        : str  (YYYY-MM-DD)
 ├── amount      : float
 ├── category    : str
 ├── description : str
 ├── to_dict()   → dict   (for CSV writing)
 └── from_dict() → Expense (from CSV row)
```

### `ExpenseTracker` class — Business Logic
```
ExpenseTracker
 ├── _load_from_csv()        reads CSV on startup
 ├── _save_to_csv()          writes all data after every change
 ├── _next_id()              auto-increments IDs
 ├── _check_budget()         warns when near/over limit
 ├── add_expense()           CRUD: create
 ├── delete_expense()        CRUD: delete
 ├── get_all_expenses()      sorted list
 ├── search_by_category()    filtered list
 ├── get_total()             grand sum
 ├── get_monthly_summary()   nested dict by month
 ├── get_category_analysis() totals per category
 └── export_summary_report() writes .txt file
```

---

## 📋 Sample CSV Data

The included `expenses.csv` contains 15 sample records across June–July 2024
so you can explore all features immediately after cloning.

---

## 🔧 Exception Handling

| Scenario | Handled By |
|---|---|
| Invalid amount (letters, negatives) | `input_amount()` — re-prompts in a loop |
| Invalid date format | `input_date()` — `strptime` validation |
| Invalid menu choice | `main()` — `if choice not in actions` guard |
| CSV file missing | `_load_from_csv()` — silent fresh start |
| File write error | `_save_to_csv()` — catches `IOError` |
| Unexpected runtime error | `main()` — broad `except Exception` |

---

## 🌱 Future Improvements

1. **SQLite backend** — replace CSV with a proper database for faster queries
2. **Rich / Colorama** — enhanced cross-platform colour support
3. **Recurring expenses** — auto-log monthly bills
4. **Data visualisation** — `matplotlib` pie/bar charts
5. **Multi-currency support** — exchange rate API integration
6. **Password protection** — encrypt the CSV with `cryptography`
7. **Web UI** — Flask/FastAPI frontend for browser access
8. **Unit tests** — `pytest` test suite for all methods
9. **Config file** — store budget and preferences in `config.json`
10. **Import bank statement** — parse PDF/OFX files automatically

---


```

### Recommended `.gitignore`
```
__pycache__/
*.pyc
expense_report.txt
```

---

## 📝 Resume / Portfolio Description

> **Expense Tracker CLI** · Python · Personal Project
> Built a terminal-based personal finance manager in Python using OOP principles
> (Expense and ExpenseTracker classes), persistent CSV storage, and a menu-driven
> interface. Features include budget warnings, category-wise analysis, monthly
> summaries, and report export. Implemented robust exception handling for invalid
> inputs and missing files. (~350 lines, PEP 8 compliant.)

---

## 📄 License

MIT — free to use, modify, and distribute.
