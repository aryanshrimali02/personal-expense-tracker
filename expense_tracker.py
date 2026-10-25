import json
import math
from datetime import datetime

# Terminal Colors
RESET = "\033[0m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
BOLD = "\033[1m"

data_file = "ExpensesData.json"
def load_expenses():
    try:
        with open(data_file, "r") as file:
            expenses = json.load(file)
            if not isinstance(expenses, list):
                print(RED + "Invalid data type, Starting with an empty list." + RESET)
                return []

            required_keys = {"amount", "category", "description", "date"}

            for expense in expenses:
                if not isinstance(expense, dict) or not required_keys.issubset(expense):
                    print(RED + "Invalid expense data, Starting with an empty list." + RESET)
                    return []
                if isinstance(expense["amount"],bool) or not isinstance(expense["amount"], (int, float)) or not math.isfinite(expense["amount"]) or expense["amount"]<=0:
                    print(RED + "Invalid amount, Starting with an empty list." + RESET)
                    return[]
                if not isinstance(expense["category"], str) or not expense["category"].strip():
                    print(RED + "Invalid category, Starting with an empty list." + RESET)
                    return[]
                if not isinstance(expense["description"], str) or not expense["description"].strip():
                    print(RED + "Invalid description, Starting with an empty list." + RESET)
                    return[]
                if not isinstance(expense["date"], str):
                    print(RED + "Invalid date, Starting with an empty list." + RESET)
                    return[]
                try:
                    datetime.strptime(expense["date"], "%d-%m-%y")
                except (ValueError,TypeError):
                    print(RED + "Invalid date value, Starting with an empty list." + RESET)
                    return[]
            print(GREEN + "Data Loaded successfully!"+ RESET)
            return expenses
    except FileNotFoundError:
        print(RED + "Data file not found, Creating new data file..." + RESET)
        return []
    except json.JSONDecodeError:
        print(RED + "Data file is corrupted. Starting with an empty list." + RESET)
        return []

expenses = load_expenses()

def main_menu():
    selection = 0
    while selection != 8:
        print(CYAN + "Personal Expense Tracker".center(80, "=") + RESET)
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
                selection = int(input(BLUE + "Enter your choice :" + RESET))
                print()
                break
            except ValueError:
                print(YELLOW + "Unknown selection, Please try again." + RESET)

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
                print(YELLOW + "Unknown selection, Please try again." + RESET)

def save_expenses():
    try:
        with open(data_file, "w") as file:
            json.dump(expenses, file, indent=4)
        return True
    except OSError:
        print(RED + "File error" + RESET)
        return False

def validate_date():
    while True:
        date = input(BLUE + "Enter Date(DD-MM-YY): " + RESET).strip()
        try:
            if date:
                datetime.strptime(date, "%d-%m-%y")
            else:
                raise ValueError
            break
        except ValueError:
            print(YELLOW + "Invalid date. Please enter a valid date in DD-MM-YY format." + RESET)
    return date
def add_expense():
    # Ask the user for the expense amount
    while True:
        try:
            exp = float(input(BLUE + "Enter expense amount: " + RESET))
            if exp <= 0 or not math.isfinite(exp):
                raise ValueError
            break
        except ValueError:
            print(YELLOW + "Amount must be greater than zero and non infinite." + RESET)
    # Ask the user for the category
    while True:
        category = input(BLUE + "Enter category: " + RESET).capitalize().strip()
        if not category:
            print(YELLOW + "Category can't be empty." + RESET)
        else:
            break
    # Ask the user for a short description
    while True:
        desc = input(BLUE + "Enter description: " + RESET).capitalize().strip()
        if not desc:
            print(YELLOW + "Description can't be empty." + RESET)
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
        print()
        print(GREEN + "Expense added successfully!" + RESET)
        print()
    else:
        expenses.pop()
def edit_expense():
    if not expenses:
        print(YELLOW + "No expenses recorded." + RESET)
        return
    else:
        print(CYAN + "All Expenses".center(60,"-") + RESET)
        
        for index, expense in enumerate(expenses, start=1):
            category = expense["category"]
            desc = expense["description"]
            amount = expense["amount"]
            date = expense["date"]
        
            print(f"{index}. {category} | {desc} | ₹{amount:,.2f} | {date}")
            print()
        while True:
            try:    
                edit_index = int(input(BLUE + "Enter the expense number you want to edit: " + RESET))
                if edit_index <= 0 or edit_index > len(expenses):
                    raise ValueError
                break
            except ValueError:
                print(YELLOW + "Please enter valid number" + RESET)

        print("1. amount")
        print("2. category")
        print("3. description")
        print("4. date")
        print()
        while True:
            try:
                selection = int(input(BLUE + "Enter the number of what you want to edit: " + RESET))
            except ValueError:
                print(YELLOW + "Enter valid number(1-4)" + RESET)
                continue
            if 0 < selection <=4:
                break
            else:
                print(YELLOW + "Enter valid number(1-4)" + RESET)
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
                        print(YELLOW + "Amount must be greater than zero and non infinite." + RESET)
            case 2:
                copy = expenses[edit_index-1]["category"]
                while True:
                        new_category = input("Enter new category: ").capitalize().strip()
                        if not new_category:
                            print(YELLOW + "Category can't be empty." + RESET)
                        else:
                            expenses[edit_index-1]["category"] = new_category
                            break
            case 3:
                copy = expenses[edit_index-1]["description"]
                while True:
                        new_desc = input(BLUE + "Enter new description: " + RESET).capitalize().strip()
                        if not new_desc:
                            print(YELLOW + "Description can't be empty." + RESET)
                        else:
                            expenses[edit_index-1]["description"] = new_desc
                            break
            case 4:
                copy = expenses[edit_index-1]["date"] 
                expenses[edit_index-1]["date"] = validate_date()
    if save_expenses():
        print(GREEN + "Changes saved successfully!" + RESET)
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
        print(YELLOW + "No expenses recorded." + RESET)
        return
    else:
        print(CYAN + "All Expenses".center(60,"-") + RESET)
    
        for index, expense in enumerate(expenses, start=1):
            category = expense["category"]
            desc = expense["description"]
            amount = expense["amount"]
            date = expense["date"]
    
            print(f"{index}. {category} | {desc} | ₹{amount:,.2f} | {date}")
            print()

        while True:
            try:
                remove_index = int(input(BLUE + "Enter the expense number you want to remove: " + RESET))
                if remove_index <= 0 or remove_index > len(expenses):
                    raise ValueError
                break
            except ValueError:
                print(YELLOW + "Please enter valid number" + RESET)
        copy = expenses[remove_index-1]
        del expenses[remove_index-1]
    if save_expenses():
        print(GREEN + "Changes saved successfully!" + RESET)
    else:
     expenses.insert(remove_index-1,copy)
def view_expenses():
    if not expenses:
        print(YELLOW + "No expenses recorded." + RESET)
    else:
        print(CYAN + "All Expenses".center(60,"-") + RESET)

        for index, expense in enumerate(expenses, start=1):
            category = expense["category"]
            desc = expense["description"]
            amount = expense["amount"]
            date = expense["date"]

            print(f"{index}. {category} | {desc} | {MAGENTA}₹{amount:,.2f}{RESET} | {date}")
            print()
            
def category_summary():
    category_totals = {}
    if not expenses:
        print(YELLOW + "No expenses recorded." + RESET)
        return
    else:
        print(CYAN + " Spending by Category ".center(60,"-") + RESET)
        for expense in expenses:
            category = expense["category"]
            amount = expense["amount"]
            if category in category_totals:
                category_totals[category] += amount
            else:
                category_totals[category] = amount
        for category, total in category_totals.items():
            print(f"{category}:{MAGENTA} ₹{total:,.2f}" + RESET)
def monthly_summary():
    monthly_total = 0
    while True:
        try:
            search_query = input(BLUE + "Enter month and year(MM-YY): " + RESET).strip()
            if search_query:
                datetime.strptime(search_query, "%m-%y")
                break
            else:
                raise ValueError
        except ValueError:
                print(YELLOW + "Invalid month. Please enter MM-YY." + RESET)
    month_empty = True
    for expense in expenses:
        date = expense["date"]
        amount = expense["amount"]
        if date[-5:] == search_query:
            monthly_total += amount
            month_empty = False
    if month_empty:
        print(YELLOW + "No expenses found for this month." + RESET)
    else:
        print(f"Total expenses for {search_query}:{MAGENTA} ₹{monthly_total:,.2f}" + RESET)

def total_expenses():
    total_amount = 0
    if not expenses:
        print(YELLOW + "No expenses recorded." + RESET)
    else:
        for expense in expenses:
            amount = expense["amount"]
            total_amount += amount
        print(f"Total expense:{MAGENTA} ₹{total_amount:,.2f}" + RESET)
        print()

main_menu()