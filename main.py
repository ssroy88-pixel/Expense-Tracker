import json
from datetime import datetime

class ExpenseTracker:
    def __init__(self, filename="expenses.json"):
        self.filename = filename
        self.expenses = []
        self.budget = {}
        self.load_data()

    # ---------------- File Handling ----------------
    def save_data(self):
        """Save expenses and budget to file."""
        data = {
            "expenses": self.expenses,
            "budget": self.budget
        }
        try:
            with open(self.filename, "w") as f:
                json.dump(data, f, indent=4)
            print("Data saved successfully.")
        except Exception as e:
            print("Error saving data:", e)

    def load_data(self):
        """Load expenses and budget from file."""
        try:
            with open(self.filename, "r") as f:
                data = json.load(f)
                self.expenses = data.get("expenses", [])
                self.budget = data.get("budget", {})
            print("Data loaded successfully.")
        except FileNotFoundError:
            print("No existing data file found. Starting fresh.")
        except Exception as e:
            print("Error loading data:", e)

    # ---------------- Expense Management ----------------
    def add_expense(self):
        """Add a new expense entry."""
        try:
            amount = float(input("Enter expense amount: ₹"))
            category = input("Enter category (e.g., Food, Travel, Bills): ").capitalize()
            date = input("Enter date (YYYY-MM-DD) or leave blank for today: ")
            if not date:
                date = datetime.now().strftime("%Y-%m-%d")

            expense = {"date": date, "category": category, "amount": amount}
            self.expenses.append(expense)
            print(f"Expense added: {category} - ₹{amount}")
        except ValueError:
            print("Invalid input. Please enter a valid amount.")

    def view_expenses(self):
        """Display all expenses."""
        if not self.expenses:
            print("No expenses recorded yet.")
            return

        print("\nAll Recorded Expenses:")
        for exp in self.expenses:
            print(f"{exp['date']} | {exp['category']} | ₹{exp['amount']}")
        print("-" * 40)
        print(f"Total Spent: ₹{self.total_expenses()}")

    def total_expenses(self):
        """Calculate total spending."""
        return sum(exp["amount"] for exp in self.expenses)

    # ---------------- Budget Management ----------------
    def set_budget(self):
        """Set a monthly budget for each category."""
        category = input("Enter category for budget: ").capitalize()
        try:
            amount = float(input(f"Enter monthly budget for {category}: "))
            self.budget[category] = amount
            print(f"Budget set for {category}: {amount}")
        except ValueError:
            print("Invalid amount. Try again.")

    def view_budget_status(self):
        """Show spending vs. budget per category."""
        if not self.budget:
            print("No budgets set yet.")
            return

        print("\nBudget Summary:")
        category_spend = {}
        for exp in self.expenses:
            cat = exp["category"]
            category_spend[cat] = category_spend.get(cat, 0) + exp["amount"]

        for cat, limit in self.budget.items():
            spent = category_spend.get(cat, 0)
            remaining = limit - spent
            status = "Within budget" if remaining >= 0 else "Over budget!"
            print(f"{cat}: Spent ₹{spent} / Budget ₹{limit} → {status}")
        print("-" * 40)

    # ---------------- Menu Interface ----------------
    def menu(self):
        """Interactive menu-driven interface."""
        while True:
            print("\n===== PERSONAL EXPENSE TRACKER =====")
            print("1. Add Expense")
            print("2. View Expenses")
            print("3. Set Monthly Budget")
            print("4. View Budget Status")
            print("5. Save Data")
            print("6. Exit")
            choice = input("Choose an option (1-6): ")

            if choice == "1":
                self.add_expense()
            elif choice == "2":
                self.view_expenses()
            elif choice == "3":
                self.set_budget()
            elif choice == "4":
                self.view_budget_status()
            elif choice == "5":
                self.save_data()
            elif choice == "6":
                self.save_data()
                print("Exiting... Have a great day!")
                break
            else:
                print("Invalid choice. Please select 1-6.")


# ---------------- Main Program ----------------
if __name__ == "__main__":
    tracker = ExpenseTracker()
    tracker.menu()
