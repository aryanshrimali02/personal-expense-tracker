import json
import math
from datetime import datetime

data_file = "ExpensesData.json"
def load_expenses():
    try:
        with open(data_file, "r") as file:
            expenses = json.load(file)
            if not isinstance(expenses, list):
                print("Invalid data type, Starting with an empty list.")
                return []

            required_keys = {"amount", "category", "description", "date"}

            for expense in expenses:
                if not isinstance(expense, dict) or not required_keys.issubset(expense):
                    print("Invalid expense data, Starting with an empty list.")
                    return []
                if isinstance(expense["amount"],bool) or not isinstance(expense["amount"], (int, float)) or not math.isfinite(expense["amount"]) or expense["amount"]<=0:
                    print("Invalid amount, Starting with an empty list.")
                    return[]
                if not isinstance(expense["category"], str) or not expense["category"].strip():
                    print("Invalid category, Starting with an empty list.")
                    return[]
                if not isinstance(expense["description"], str) or not expense["description"].strip():
                    print("Invalid description, Starting with an empty list.")
                    return[]
                if not isinstance(expense["date"], str):
                    print("Invalid date, Starting with an empty list.")
                    return[]
                try:
                    datetime.strptime(expense["date"], "%d-%m-%y")
                except (ValueError,TypeError):
                    print("Invalid date value, Starting with an empty list.")
                    return[]
            print("Data Loaded successfully")
            return expenses
    except FileNotFoundError:
        print("Data file not found")
        return []
    except json.JSONDecodeError:
        print("Data file is corrupted. Starting with an empty list.")
        return []

expenses = load_expenses()

def main_menu():
    selection = 0
    while selection != 8:
        print("Personal Expense Tracker".center(80, "="))
        print("1. Add Expense")
        print("2. View Expense")
        print("3. Show total Expenses")
        print("4. Spending by Category")
        print("5. Search by Month")
        print("6. Remove expense")
        print("7. Edit expense")
        print("8. Exit")
        print()
        while True:
            try:
                selection = int(input("Enter your choice :"))
                print()
                break
            except ValueError:
                print("Unknown selection, Please try again.")

        match selection:
            case 1:
                add_expense()
            case 2:
                view_expenses()
            case 3:
                total_expenses()
            case 4:
                category_summary()
            case 5:
                monthly_summary()
            case 6:
                remove_expense()
            case 7:
                edit_expense()
            case 8:
                print("Exiting...")
            case _:
                print("Unknown selection, Please try again.")

def save_expenses():
    try:
        with open(data_file, "w") as file:
            json.dump(expenses, file, indent=4)
        return True
    except OSError:
        print("File error")
        return False

def validate_date():
    while True:
        date = input("Enter Date(DD-MM-YY): ").strip()
        try:
            if date:
                datetime.strptime(date, "%d-%m-%y")
            else:
                raise ValueError
            break
        except ValueError:
            print("Invalid date. Please enter a valid date in DD-MM-YY format.")
    return date
def add_expense():
    # Ask the user for the expense amount
    while True:
        try:
            exp = float(input("Enter expense amount: "))
            if exp <= 0 or not math.isfinite(exp):
                raise ValueError
            break
        except ValueError:
            print("Amount must be greater than zero and non infinite.")
    # Ask the user for the category
    while True:
        category = input("Enter category: ").capitalize().strip()
        if not category:
            print("Category can't be empty.")
        else:
            break
    # Ask the user for a short description
    while True:
        desc = input("Enter description: ").capitalize().strip()
        if not desc:
            print("Description can't be empty.")
        else:
            break
    # Ask the user for date
    date = validate_date()
    # Create a dictionary containing the expense
    expense = {
        "amount":exp,
        "category":category,
        "description":desc,
        "date":date
    }
    # Add that dictionary to the expenses list
    expenses.append(expense)
    if save_expenses():
        print("Expense added successfully!")
    else:
        expenses.pop()
def edit_expense():
    if not expenses:
        print("No expenses recorded.")
        return
    else:
        print("All Expenses".center(60,"-"))
        
        for index, expense in enumerate(expenses, start=1):
            category = expense["category"]
            desc = expense["description"]
            amount = expense["amount"]
            date = expense["date"]
        
            print(f"{index}. {category} | {desc} | ₹{amount:,.2f} | {date}")
            print()
        while True:
            try:    
                edit_index = int(input("Enter the expense number you want to edit: "))
                if edit_index <= 0 or edit_index > len(expenses):
                    raise ValueError
                break
            except ValueError:
                print("Please enter valid number")

        print("1. amount")
        print("2. category")
        print("3. description")
        print("4. date")
        print()
        while True:
            try:
                selection = int(input("Enter the number of what you want to edit: "))
            except ValueError:
                print("Enter valid number(1-4)")
                continue
            if 0 < selection <=4:
                break
            else:
                print("Enter valid number(1-4)")
        match selection:
            case 1:
                copy = expenses[edit_index-1]["amount"]
                while True:
                    try:
                        amo = float(input("Enter new amount: "))
                        if amo <= 0 or not math.isfinite(amo):
                            raise ValueError
                        expenses[edit_index-1]["amount"] = amo
                        break
                    except ValueError:
                        print("Amount must be greater than zero and non infinite.")
            case 2:
                copy = expenses[edit_index-1]["category"]
                while True:
                        new_category = input("Enter new category: ").capitalize().strip()
                        if not new_category:
                            print("Category can't be empty.")
                        else:
                            expenses[edit_index-1]["category"] = new_category
                            break
            case 3:
                copy = expenses[edit_index-1]["description"]
                while True:
                        new_desc = input("Enter new description: ").capitalize().strip()
                        if not new_desc:
                            print("Description can't be empty.")
                        else:
                            expenses[edit_index-1]["description"] = new_desc
                            break
            case 4:
                copy = expenses[edit_index-1]["date"] 
                expenses[edit_index-1]["date"] = validate_date()
    if save_expenses():
        print("Changes saved successfully!")
    else:
        match selection:
            case 1:
                expenses[edit_index-1]["amount"] = copy
            case 2:
                expenses[edit_index-1]["category"] = copy
            case 3:
                expenses[edit_index-1]["description"] = copy
            case 4:
                expenses[edit_index-1]["date"] = copy

def remove_expense():
    if not expenses:
        print("No expenses recorded.")
        return
    else:
        print("All Expenses".center(60,"-"))
    
        for index, expense in enumerate(expenses, start=1):
            category = expense["category"]
            desc = expense["description"]
            amount = expense["amount"]
            date = expense["date"]
    
            print(f"{index}. {category} | {desc} | ₹{amount:,.2f} | {date}")
            print()

        while True:
            try:
                remove_index = int(input("Enter the expense number you want to remove: "))
                if remove_index <= 0 or remove_index > len(expenses):
                    raise ValueError
                break
            except ValueError:
                print("Please enter valid number")
        copy = expenses[remove_index-1]
        del expenses[remove_index-1]
    if save_expenses():
        print("Changes saved successfully!")
    else:
     expenses.insert(remove_index-1,copy)
def view_expenses():
    if not expenses:
        print("No expenses recorded.")
    else:
        print("All Expenses".center(60,"-"))

        for index, expense in enumerate(expenses, start=1):
            category = expense["category"]
            desc = expense["description"]
            amount = expense["amount"]
            date = expense["date"]

            print(f"{index}. {category} | {desc} | ₹{amount:,.2f} | {date}")
            print()
            
def category_summary():
    category_totals = {}
    if not expenses:
        print("No expenses recorded.")
        return
    else:
        print(" Spending by Category ".center(60,"-"))
        for expense in expenses:
            category = expense["category"]
            amount = expense["amount"]
            if category in category_totals:
                category_totals[category] += amount
            else:
                category_totals[category] = amount
        for category, total in category_totals.items():
            print(f"{category}: ₹{total:,.2f}")
def monthly_summary():
    monthly_total = 0
    while True:
        try:
            search_query = input("Enter month and year(MM-YY): ").strip()
            if search_query:
                datetime.strptime(search_query, "%m-%y")
                break
            else:
                raise ValueError
        except ValueError:
                print("Invalid month. Please enter MM-YY.")
    month_empty = True
    for expense in expenses:
        date = expense["date"]
        amount = expense["amount"]
        if date[-5:] == search_query:
            monthly_total += amount
            month_empty = False
    if month_empty:
        print("No expenses found for this month.")
    else:
        print(f"Total expenses for {search_query}: ₹{monthly_total:,.2f}")

def total_expenses():
    total_amount = 0
    if not expenses:
        print("No expenses recorded.")
    else:
        for expense in expenses:
            amount = expense["amount"]
            total_amount += amount
        print(f"Total expense: ₹{total_amount:,.2f}")
        print()

main_menu()