"""
============================================================
  Expense Tracker - CLI-based Personal Finance Manager
  Author  : Your Name
  Version : 1.0.0
  Python  : 3.8+
============================================================
A beginner-to-intermediate portfolio project demonstrating:
  - Object-Oriented Programming (OOP)
  - File I/O with CSV
  - Exception handling
  - Clean CLI interface
  - Budget warnings & monthly analytics
"""

import csv
import os
from datetime import datetime
from collections import defaultdict


# ── Constants ──────────────────────────────────────────────────────────────────

CSV_FILE = "expenses.csv"
REPORT_FILE = "expense_report.txt"

CATEGORIES = ["Food", "Travel", "Shopping", "Bills", "Entertainment", "Other"]

CSV_HEADERS = ["id", "date", "amount", "category", "description"]

# Default monthly budget limit (₹ / your currency)
DEFAULT_BUDGET = 10000.00

# ANSI colour codes for a polished terminal look
RED    = "\033[91m"
GREEN  = "\033[92m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"
BOLD   = "\033[1m"
RESET  = "\033[0m"


# ── Expense (Data Model) ───────────────────────────────────────────────────────

class Expense:
    """
    Represents a single expense entry.

    Attributes:
        expense_id  (int)   : Unique identifier (auto-assigned).
        date        (str)   : Date of the expense (YYYY-MM-DD).
        amount      (float) : Amount spent.
        category    (str)   : One of the predefined CATEGORIES.
        description (str)   : Short description of the expense.
    """

    def __init__(self, expense_id: int, date: str, amount: float,
                 category: str, description: str):
        self.expense_id  = expense_id
        self.date        = date
        self.amount      = float(amount)
        self.category    = category
        self.description = description

    # ── Serialisation helpers ──────────────────────────────────────────────────

    def to_dict(self) -> dict:
        """Return a dict suitable for writing to CSV."""
        return {
            "id"         : self.expense_id,
            "date"       : self.date,
            "amount"     : f"{self.amount:.2f}",
            "category"   : self.category,
            "description": self.description,
        }

    @classmethod
    def from_dict(cls, row: dict) -> "Expense":
        """Create an Expense instance from a CSV row (dict)."""
        return cls(
            expense_id  = int(row["id"]),
            date        = row["date"],
            amount      = float(row["amount"]),
            category    = row["category"],
            description = row["description"],
        )

    # ── Display helper ─────────────────────────────────────────────────────────

    def __str__(self) -> str:
        return (
            f"[{self.expense_id:>4}] {self.date}  "
            f"{CYAN}{self.category:<15}{RESET}"
            f"₹{self.amount:>10,.2f}  {self.description}"
        )


# ── ExpenseTracker (Business Logic) ───────────────────────────────────────────

class ExpenseTracker:
    """
    Manages all expense operations: CRUD, search, analytics, export.

    Attributes:
        csv_file (str)   : Path to the CSV data file.
        budget   (float) : Monthly spending limit for warnings.
        expenses (list)  : In-memory list of Expense objects.
    """

    def __init__(self, csv_file: str = CSV_FILE,
                 budget: float = DEFAULT_BUDGET):
        self.csv_file = csv_file
        self.budget   = budget
        self.expenses: list[Expense] = []
        self._load_from_csv()

    # ── Private helpers ────────────────────────────────────────────────────────

    def _load_from_csv(self) -> None:
        """Load expenses from the CSV file into memory."""
        if not os.path.exists(self.csv_file):
            return  # Fresh start — file will be created on first save

        try:
            with open(self.csv_file, "r", newline="", encoding="utf-8") as fh:
                reader = csv.DictReader(fh)
                for row in reader:
                    self.expenses.append(Expense.from_dict(row))
        except FileNotFoundError:
            print(f"{YELLOW}⚠  Data file not found. Starting fresh.{RESET}")
        except Exception as exc:
            print(f"{RED}✗  Error reading CSV: {exc}{RESET}")

    def _save_to_csv(self) -> None:
        """Persist all in-memory expenses to the CSV file."""
        try:
            with open(self.csv_file, "w", newline="", encoding="utf-8") as fh:
                writer = csv.DictWriter(fh, fieldnames=CSV_HEADERS)
                writer.writeheader()
                for expense in self.expenses:
                    writer.writerow(expense.to_dict())
        except IOError as exc:
            print(f"{RED}✗  Could not save data: {exc}{RESET}")

    def _next_id(self) -> int:
        """Generate the next available expense ID."""
        return max((e.expense_id for e in self.expenses), default=0) + 1

    def _current_month_total(self) -> float:
        """Return total spending for the current calendar month."""
        now = datetime.now()
        return sum(
            e.amount for e in self.expenses
            if e.date.startswith(f"{now.year}-{now.month:02d}")
        )

    def _check_budget(self) -> None:
        """Print a warning if monthly spending is near or over budget."""
        total = self._current_month_total()
        pct   = (total / self.budget) * 100 if self.budget else 0

        if total >= self.budget:
            print(f"\n{RED}{BOLD}⚠  BUDGET EXCEEDED! "
                  f"Spent ₹{total:,.2f} of ₹{self.budget:,.2f} "
                  f"({pct:.1f}%){RESET}")
        elif pct >= 80:
            print(f"\n{YELLOW}⚠  Budget warning: {pct:.1f}% used "
                  f"(₹{total:,.2f} / ₹{self.budget:,.2f}){RESET}")

    # ── CRUD operations ────────────────────────────────────────────────────────

    def add_expense(self, date: str, amount: float,
                    category: str, description: str) -> Expense:
        """Create, store and return a new Expense."""
        expense = Expense(
            expense_id  = self._next_id(),
            date        = date,
            amount      = amount,
            category    = category,
            description = description,
        )
        self.expenses.append(expense)
        self._save_to_csv()
        self._check_budget()
        return expense

    def delete_expense(self, expense_id: int) -> bool:
        """Remove an expense by ID. Returns True if deleted."""
        for i, expense in enumerate(self.expenses):
            if expense.expense_id == expense_id:
                del self.expenses[i]
                self._save_to_csv()
                return True
        return False

    # ── Query / analytics ──────────────────────────────────────────────────────

    def get_all_expenses(self) -> list[Expense]:
        """Return all expenses sorted by date (newest first)."""
        return sorted(self.expenses, key=lambda e: e.date, reverse=True)

    def search_by_category(self, category: str) -> list[Expense]:
        """Return expenses matching the given category."""
        return [e for e in self.expenses
                if e.category.lower() == category.lower()]

    def get_total(self) -> float:
        """Return the grand total of all expenses."""
        return sum(e.amount for e in self.expenses)

    def get_monthly_summary(self) -> dict:
        """
        Return a nested dict:
            { "YYYY-MM": { "total": float, "by_category": { cat: float } } }
        """
        summary: dict = defaultdict(lambda: {"total": 0.0,
                                              "by_category": defaultdict(float)})
        for expense in self.expenses:
            month = expense.date[:7]  # "YYYY-MM"
            summary[month]["total"] += expense.amount
            summary[month]["by_category"][expense.category] += expense.amount

        # Sort months chronologically
        return dict(sorted(summary.items()))

    def get_category_analysis(self) -> dict:
        """Return total spending per category across all time."""
        analysis: dict = defaultdict(float)
        for expense in self.expenses:
            analysis[expense.category] += expense.amount
        return dict(sorted(analysis.items(), key=lambda x: x[1], reverse=True))

    def export_summary_report(self, filepath: str = REPORT_FILE) -> str:
        """Write a human-readable summary report to a .txt file."""
        lines = []
        now   = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        lines.append("=" * 60)
        lines.append("         EXPENSE TRACKER — SUMMARY REPORT")
        lines.append(f"         Generated : {now}")
        lines.append("=" * 60)

        lines.append(f"\nTotal Expenses  : ₹{self.get_total():,.2f}")
        lines.append(f"Total Records   : {len(self.expenses)}")
        lines.append(f"Monthly Budget  : ₹{self.budget:,.2f}")

        lines.append("\n── Category-wise Spending ──────────────────────────")
        for cat, total in self.get_category_analysis().items():
            pct = (total / self.get_total() * 100) if self.get_total() else 0
            lines.append(f"  {cat:<15}  ₹{total:>10,.2f}  ({pct:5.1f}%)")

        lines.append("\n── Monthly Summary ─────────────────────────────────")
        for month, data in self.get_monthly_summary().items():
            lines.append(f"\n  {month}  —  Total: ₹{data['total']:,.2f}")
            for cat, amt in sorted(data["by_category"].items()):
                lines.append(f"      {cat:<15} ₹{amt:,.2f}")

        lines.append("\n── All Expenses ────────────────────────────────────")
        for expense in self.get_all_expenses():
            lines.append(
                f"  [{expense.expense_id:>4}] {expense.date}  "
                f"{expense.category:<15} ₹{expense.amount:>10,.2f}  "
                f"{expense.description}"
            )

        lines.append("\n" + "=" * 60)

        try:
            with open(filepath, "w", encoding="utf-8") as fh:
                fh.write("\n".join(lines))
            return filepath
        except IOError as exc:
            raise IOError(f"Could not write report: {exc}") from exc


# ── CLI helpers ────────────────────────────────────────────────────────────────

def clear_screen() -> None:
    """Clear the terminal (cross-platform)."""
    os.system("cls" if os.name == "nt" else "clear")


def print_header() -> None:
    """Print the application banner."""
    print(f"\n{CYAN}{BOLD}{'=' * 52}")
    print("       💰  EXPENSE TRACKER  v1.0")
    print(f"{'=' * 52}{RESET}\n")


def print_menu() -> None:
    """Display the main menu."""
    options = [
        ("1", "Add Expense"),
        ("2", "View All Expenses"),
        ("3", "Search by Category"),
        ("4", "Show Total Expenses"),
        ("5", "Monthly Summary"),
        ("6", "Category Analysis"),
        ("7", "Delete Expense"),
        ("8", "Export Summary Report"),
        ("9", "Set Budget Limit"),
        ("0", "Exit"),
    ]
    print(f"{BOLD}  MAIN MENU{RESET}")
    print("  " + "─" * 30)
    for key, label in options:
        print(f"  [{key}] {label}")
    print("  " + "─" * 30)


def input_date() -> str:
    """Prompt for a valid date; default = today."""
    today = datetime.now().strftime("%Y-%m-%d")
    while True:
        raw = input(f"  Date (YYYY-MM-DD) [{today}]: ").strip()
        if not raw:
            return today
        try:
            datetime.strptime(raw, "%Y-%m-%d")
            return raw
        except ValueError:
            print(f"  {RED}Invalid date format. Use YYYY-MM-DD.{RESET}")


def input_amount() -> float:
    """Prompt for a positive float amount."""
    while True:
        raw = input("  Amount (₹): ").strip()
        try:
            amount = float(raw)
            if amount <= 0:
                raise ValueError
            return amount
        except ValueError:
            print(f"  {RED}Please enter a valid positive number.{RESET}")


def input_category() -> str:
    """Display category menu and return a valid selection."""
    print("  Categories:")
    for i, cat in enumerate(CATEGORIES, 1):
        print(f"    [{i}] {cat}")
    while True:
        raw = input("  Choose category (1-6): ").strip()
        try:
            idx = int(raw) - 1
            if 0 <= idx < len(CATEGORIES):
                return CATEGORIES[idx]
            raise ValueError
        except ValueError:
            print(f"  {RED}Enter a number between 1 and {len(CATEGORIES)}.{RESET}")


def separator() -> None:
    print(f"\n{CYAN}{'─' * 52}{RESET}\n")


# ── Menu action functions ──────────────────────────────────────────────────────

def action_add_expense(tracker: ExpenseTracker) -> None:
    """Collect input and add a new expense."""
    print(f"\n{BOLD}  ➕  ADD EXPENSE{RESET}")
    separator()

    date        = input_date()
    amount      = input_amount()
    category    = input_category()
    description = input("  Description: ").strip() or "No description"

    expense = tracker.add_expense(date, amount, category, description)
    print(f"\n  {GREEN}✔  Expense added:{RESET}\n  {expense}")


def action_view_all(tracker: ExpenseTracker) -> None:
    """Print all expenses in a formatted table."""
    print(f"\n{BOLD}  📋  ALL EXPENSES{RESET}")
    separator()

    expenses = tracker.get_all_expenses()
    if not expenses:
        print("  No expenses recorded yet.")
        return

    print(f"  {'ID':>4}  {'Date':<12} {'Category':<15} {'Amount':>12}  Description")
    print("  " + "─" * 65)
    for e in expenses:
        print(f"  {e.expense_id:>4}  {e.date:<12} "
              f"{CYAN}{e.category:<15}{RESET}"
              f"₹{e.amount:>10,.2f}  {e.description}")
    print("  " + "─" * 65)
    print(f"  {'TOTAL':>32}  ₹{tracker.get_total():>10,.2f}")


def action_search_category(tracker: ExpenseTracker) -> None:
    """Search and display expenses for a chosen category."""
    print(f"\n{BOLD}  🔍  SEARCH BY CATEGORY{RESET}")
    separator()
    category = input_category()

    results = tracker.search_by_category(category)
    if not results:
        print(f"  No expenses found for '{category}'.")
        return

    total = sum(e.amount for e in results)
    print(f"\n  {CYAN}{category}{RESET} — {len(results)} record(s)\n")
    for e in results:
        print(f"    {e.date}  ₹{e.amount:>10,.2f}  {e.description}")
    print(f"\n  Subtotal: ₹{total:,.2f}")


def action_show_total(tracker: ExpenseTracker) -> None:
    """Show grand total and a quick per-category breakdown."""
    print(f"\n{BOLD}  💵  TOTAL EXPENSES{RESET}")
    separator()
    print(f"  Grand Total : {GREEN}₹{tracker.get_total():,.2f}{RESET}")
    print(f"  Records     : {len(tracker.expenses)}\n")

    analysis = tracker.get_category_analysis()
    grand    = tracker.get_total() or 1  # avoid div/0
    if analysis:
        print(f"  {'Category':<15} {'Amount':>12}  {'Share':>6}")
        print("  " + "─" * 38)
        for cat, amt in analysis.items():
            bar = "█" * int((amt / grand) * 20)
            print(f"  {cat:<15} ₹{amt:>10,.2f}  {bar}")


def action_monthly_summary(tracker: ExpenseTracker) -> None:
    """Print month-by-month spending with category breakdown."""
    print(f"\n{BOLD}  📅  MONTHLY SUMMARY{RESET}")
    separator()

    summary = tracker.get_monthly_summary()
    if not summary:
        print("  No data available.")
        return

    for month, data in summary.items():
        print(f"  {CYAN}{BOLD}{month}{RESET}  —  ₹{data['total']:,.2f}")
        for cat, amt in sorted(data["by_category"].items()):
            print(f"      {cat:<15} ₹{amt:,.2f}")
        print()


def action_category_analysis(tracker: ExpenseTracker) -> None:
    """Show category-wise spending with a visual ASCII bar chart."""
    print(f"\n{BOLD}  📊  CATEGORY ANALYSIS{RESET}")
    separator()

    analysis = tracker.get_category_analysis()
    if not analysis:
        print("  No data available.")
        return

    grand = tracker.get_total() or 1
    print(f"  {'Category':<15} {'Amount':>12}  {'%':>5}  Chart")
    print("  " + "─" * 55)
    for cat, amt in analysis.items():
        pct  = (amt / grand) * 100
        bars = "█" * int(pct / 2.5)
        print(f"  {cat:<15} ₹{amt:>10,.2f}  {pct:5.1f}%  {CYAN}{bars}{RESET}")


def action_delete_expense(tracker: ExpenseTracker) -> None:
    """Delete an expense by its ID."""
    print(f"\n{BOLD}  🗑  DELETE EXPENSE{RESET}")
    separator()

    raw = input("  Enter Expense ID to delete: ").strip()
    try:
        expense_id = int(raw)
    except ValueError:
        print(f"  {RED}Invalid ID.{RESET}")
        return

    confirm = input(f"  Delete expense #{expense_id}? (y/n): ").strip().lower()
    if confirm != "y":
        print("  Cancelled.")
        return

    if tracker.delete_expense(expense_id):
        print(f"  {GREEN}✔  Expense #{expense_id} deleted.{RESET}")
    else:
        print(f"  {RED}✗  Expense #{expense_id} not found.{RESET}")


def action_export_report(tracker: ExpenseTracker) -> None:
    """Export a full summary report to a text file."""
    print(f"\n{BOLD}  📤  EXPORT REPORT{RESET}")
    separator()

    filepath = input(f"  Save as [{REPORT_FILE}]: ").strip() or REPORT_FILE
    try:
        saved = tracker.export_summary_report(filepath)
        print(f"  {GREEN}✔  Report saved to: {saved}{RESET}")
    except IOError as exc:
        print(f"  {RED}✗  {exc}{RESET}")


def action_set_budget(tracker: ExpenseTracker) -> None:
    """Update the monthly budget limit."""
    print(f"\n{BOLD}  ⚙  SET BUDGET LIMIT{RESET}")
    separator()
    print(f"  Current monthly budget: ₹{tracker.budget:,.2f}")

    raw = input("  New budget (₹): ").strip()
    try:
        budget = float(raw)
        if budget <= 0:
            raise ValueError
        tracker.budget = budget
        print(f"  {GREEN}✔  Budget updated to ₹{budget:,.2f}{RESET}")
    except ValueError:
        print(f"  {RED}Invalid amount.{RESET}")


# ── Main entry point ───────────────────────────────────────────────────────────

def main() -> None:
    """Application entry point — runs the CLI loop."""
    tracker = ExpenseTracker()

    actions = {
        "1": action_add_expense,
        "2": action_view_all,
        "3": action_search_category,
        "4": action_show_total,
        "5": action_monthly_summary,
        "6": action_category_analysis,
        "7": action_delete_expense,
        "8": action_export_report,
        "9": action_set_budget,
    }

    while True:
        clear_screen()
        print_header()
        print_menu()

        choice = input("\n  Enter your choice: ").strip()

        if choice == "0":
            print(f"\n  {GREEN}Goodbye! Keep tracking your expenses. 👋{RESET}\n")
            break

        if choice not in actions:
            print(f"\n  {RED}Invalid choice. Please enter 0–9.{RESET}")
            input("\n  Press Enter to continue…")
            continue

        try:
            actions[choice](tracker)
        except KeyboardInterrupt:
            print(f"\n  {YELLOW}Action cancelled.{RESET}")
        except Exception as exc:
            print(f"\n  {RED}Unexpected error: {exc}{RESET}")

        input(f"\n  {YELLOW}Press Enter to return to menu…{RESET}")


if __name__ == "__main__":
    main()
