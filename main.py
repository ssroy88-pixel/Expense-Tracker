import json
from datetime import datetime

class ExpenseTracker:
    def __init__(self, filename="expenses.json"):
        self.filename = filename
        self.data = {
            "expenses": [],
            "budgets": {}
        }
        self.load_data()

    # -------------------- FILE HANDLING --------------------
    def save_data(self):
        try:
            with open(self.filename, "w") as f:
                json.dump(self.data, f, indent=4)
            print("✔ Auto-saved successfully.")
        except Exception as e:
            print("Error saving file:", e)

    def load_data(self):
        try:
            with open(self.filename, "r") as f:
                self.data = json.load(f)
            print("Data loaded successfully!")
        except FileNotFoundError:
            print("No previous data found. Starting fresh.")
        except Exception as e:
            print("Error loading file:", e)

    # -------------------- EXPENSE FUNCTIONS --------------------
    def add_expense(self):
        try:
            amount = float(input("Enter amount: "))
            category = input("Enter category (Food, Travel, etc.): ")
            description = input("Enter description: ")

            # Ask user for date
            date_input = input("Enter date (DD-MM-YYYY) or press Enter for today: ")

            if date_input.strip() == "":
                # Use today's date
                date_str = datetime.now().strftime("%d-%m-%Y")
            else:
                # Validate and parse entered date
                try:
                    date_obj = datetime.strptime(date_input, "%d-%m-%Y")
                    date_str = date_obj.strftime("%d-%m-%Y")
                except:
                    print("Invalid date format! Use DD-MM-YYYY.")
                    return

            # Extract month name from entered date
            if date_input.strip() == "":
                month_name = datetime.now().strftime("%B")
            else:
                month_name = date_obj.strftime("%B")

            # Create the expense entry
            expense = {
                "amount": amount,
                "category": category,
                "description": description,
                "date": date_str,
                "month": month_name
            }

            self.data["expenses"].append(expense)
            print("Expense added successfully!")

            # AUTO-SAVE
            self.save_data()

        except Exception as e:
            print("Error adding expense:", e)

    def view_expenses(self):
        if not self.data["expenses"]:
            print("No expenses found.")
            return

        print("\n---- All Expenses ----")
        for i, exp in enumerate(self.data["expenses"], start=1):
            print(f"{i}. {exp['date']} | {exp['category']} | Rs.{exp['amount']} | {exp['description']}")

    def delete_expense(self):
        self.view_expenses()
        try:
            index = int(input("Enter the expense number to delete: "))
            if 1 <= index <= len(self.data["expenses"]):
                removed = self.data["expenses"].pop(index - 1)
                print("Deleted:", removed)

                # AUTO-SAVE
                self.save_data()

            else:
                print("Invalid number.")
        except:
            print("Invalid input.")

    def edit_expense(self):
        self.view_expenses()

        try:
            index = int(input("Enter the expense number to edit: "))
            if not (1 <= index <= len(self.data["expenses"])):
                print("Invalid choice.")
                return

            exp = self.data["expenses"][index - 1]
            print("\nEditing Expense:")
            print("Leave blank to keep old value.")

            # Show existing values
            print(f"Current Amount: {exp['amount']}")
            print(f"Current Category: {exp['category']}")
            print(f"Current Description: {exp['description']}\n")

            new_amount = input("New Amount: ")
            new_category = input("New Category: ")
            new_desc = input("New Description: ")

            # Apply edits
            if new_amount.strip():
                exp['amount'] = float(new_amount)
            if new_category.strip():
                exp['category'] = new_category
            if new_desc.strip():
                exp['description'] = new_desc

            print("Expense updated successfully!")

            # AUTO-SAVE
            self.save_data()

        except Exception as e:
            print("Invalid input. Error:", e)

    # -------------------- BUDGET FUNCTIONS --------------------
    def set_monthly_budget(self):
        month = input("Enter month name (e.g., January): ").capitalize()
        try:
            amount = float(input("Enter monthly budget: "))
            self.data["budgets"][month] = amount
            print(f"Budget set for {month}: Rs.{amount}")

            # AUTO-SAVE
            self.save_data()

        except:
            print("Invalid amount.")

    def view_monthly_report(self):
        month = input("Enter month name to view report: ").capitalize()

        # Filter expenses for that month
        expenses = [exp for exp in self.data["expenses"] if exp["month"] == month]
        total_spent = sum(exp["amount"] for exp in expenses)
        budget = self.data["budgets"].get(month, None)

        print("\n===== Monthly Report =====")
        print(f"Month: {month}")
        print(f"Total Spent: Rs.{total_spent}")

        # ----------- CATEGORY BREAKDOWN -----------
        print("\n--- Category-wise Breakdown ---")
        if expenses:
            category_summary = {}

            for exp in expenses:
                cat = exp["category"]
                amt = exp["amount"]
                category_summary[cat] = category_summary.get(cat, 0) + amt

            for cat, amt in category_summary.items():
                print(f"{cat}: Rs.{amt}")
        else:
            print("No expenses for this month.")

        # ----------- BUDGET SUMMARY -----------
        print("\n--- Budget Status ---")
        if budget:
            remaining = budget - total_spent

            print(f"Budget: Rs.{budget}")
            print(f"Remaining Balance: Rs.{remaining}")

            if remaining < 0:
                print("You exceeded your budget!")
            else:
                print("You are within the budget.")
        else:
            print("No budget set for this month.")

    # -------------------- MAIN MENU --------------------
    def menu(self):
        while True:
            print("\n===== Expense Tracker Menu =====")
            print("1. Add Expense")
            print("2. View Expenses")
            print("3. Edit Expense")
            print("4. Delete Expense")
            print("5. Set Monthly Budget")
            print("6. View Monthly Report")
            print("7. Exit")

            choice = input("Enter your choice: ")

            if choice == "1":
                self.add_expense()
            elif choice == "2":
                self.view_expenses()
            elif choice == "3":
                self.edit_expense()
            elif choice == "4":
                self.delete_expense()
            elif choice == "5":
                self.set_monthly_budget()
            elif choice == "6":
                self.view_monthly_report()
            elif choice == "7":
                print("Exiting...")
                break
            else:
                print("Invalid choice. Try again.")


# -------------------- RUN THE PROGRAM --------------------
tracker = ExpenseTracker()
tracker.menu()
