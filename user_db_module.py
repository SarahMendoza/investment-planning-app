
import calendar
import uuid
from datetime import datetime, timedelta

import portfolio_calcs as pc

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os

os.environ['MONGODB_PASS'] = 'pass'

if "MONGODB_PASS" in os.environ:
    uri = "insert URI here".format(os.environ["MONGODB_PASS"])
else:
    raise "MONGODB_PASS not in environment"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = client["Investment-Planning-App"]
#collection = db["movies"]

import requests

API_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NDM4OTY0NDcsImlhdCI6MTc0Mzg5Mjg0Nywic3ViIjoidXNlcl9pZCJ9.CMmJZHb1qqTZxN5yYOiAG9IkYG9rs92Q4J40vNh2PA8'
BASE_URL = 'http://localhost:5000/api/v1'

headers = {
    'Authorization': f'Bearer {API_KEY}'
}

# # Analyze single stock
# response = requests.get(
#     f'{BASE_URL}/analyze/AAPL',
#     headers=headers
# )
# print(response.json())

# # Batch analysis
# response = requests.post(
#     f'{BASE_URL}/analyze/batch',
#     headers=headers,
#     json={'tickers': ['AAPL', 'GOOGL', 'MSFT']}
# )
# print(response.json())

def calculate_age(dob_string):
    # Convert the string into a datetime object
    dob = datetime.strptime(dob_string, "%d-%m-%Y")

    # Get the current date
    today = datetime.today()

    # Calculate the difference in years
    age = today.year - dob.year

    # Adjust age if the birthday hasn't occurred yet this year
    if (today.month, today.day) < (dob.month, dob.day):
        age -= 1

    return age


#static functions for database operations
def create_user(db, user_name, first_name, last_name, email, password, dob, monthly_income = 0):
    age = calculate_age(dob)
    user = {
        "user_name": user_name,
        "password": password,
        "age": age,
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "monthly_income": monthly_income
    }
    db.users.insert_one(user) 

def get_user(db, user_name):
    user = db.users.find_one({"user_name": user_name})
    if user:
        return {
            "user_name": user["user_name"],
            "first_name": user["first_name"],
            "last_name": user["last_name"],
            "email": user["email"],
            "monthly_income": user["monthly_income"]
        }
    else:
        return None
    
def update_user(db, user_name, field_to_update, new_value):
    user = db.users.find_one({"user_name": user_name})
    if user:
        # Check if the field to update exists in the user document
        if field_to_update in user:
            # Update the specified field
            db.users.update_one(
                {"user_name": user_name},
                {"$set": {field_to_update: new_value}}
            )
            print(f"User '{user_name}' updated successfully. {field_to_update} is now {new_value}.")
        else:
            print(f"Field '{field_to_update}' does not exist in the user document.")
    else:
        print("User not found.")

def delete_user(db, user_name):
    user = db.users.find_one({"user_name": user_name})
    if user:
        # Remove the user from the database
        db.users.delete_one({"user_name": user_name})
        print(f"User '{user_name}' deleted successfully.")
    else:
        print("User not found.")

def create_portfolio(db, user_name, time_horizon, investment_amount, investment_split = [], stocks=[]):
    user = db.users.find_one({"user_name": user_name})
    if user:
        # Check if the user already has a portfolio
        if "portfolio" in user:
            # If portfolio exists, we update it rather than adding a new one
            print("User already has a portfolio. Updating the existing portfolio.")
            # Calculate risk and return rate if stocks are provided
            if len(stocks) > 0:
                risk, return_rate = pc.calculate_portfolio_performance(stocks, investment_split)
            else:
                risk = 0
                return_rate = 0

            # Update the portfolio
            updated_portfolio = {
                "stocks": stocks,
                "risk": risk,
                "return_rate": return_rate,
                "time_horizon": time_horizon,
                "investment_amount": investment_amount,
                "investment_split": investment_split
            }
            db.users.update_one({"user_name": user_name}, {"$set": {"portfolio": updated_portfolio}})
            print("Portfolio updated successfully.")
        else:
            # If no portfolio exists, create a new one
            print("Creating new portfolio for the user.")
            # Calculate risk and return rate if stocks are provided
            if len(stocks) > 0:
                risk, return_rate = pc.calculate_portfolio_performance(stocks, investment_split)
            else:
                risk = 0
                return_rate = 0

            # Create the new portfolio
            new_portfolio = {
                "stocks": stocks,
                "risk": risk,
                "return_rate": return_rate,
                "time_horizon": time_horizon,
                "investment_amount": investment_amount,
                "investment_split": investment_split
            }

            # Set the portfolio field with the new portfolio data
            db.users.update_one({"user_name": user_name}, {"$set": {"portfolio": new_portfolio}})
            print("Portfolio created successfully.")
    else:
        print("User not found.")

def update_stock_portfolio(db, user_name, field_to_update, new_value):
    user = db.users.find_one({"user_name": user_name})
    if user:
        # Check if the user has a portfolio
        if "portfolio" in user:
            portfolio = user["portfolio"]
            
            # Prepare the update based on the field_to_update
            if field_to_update in portfolio:
                # Update the specified field
                db.users.update_one(
                    {"user_name": user_name},
                    {"$set": {f"portfolio.{field_to_update}": new_value}}
                )
                print(f"Portfolio updated successfully. {field_to_update} is now {new_value}.")
            else:
                print(f"Field '{field_to_update}' does not exist in the portfolio.")
        else:
            print("User does not have a portfolio.")
    else:
        print("User not found.")

def add_stock(db, user_name, stock_name, stock_amount):
    user = db.users.find_one({"user_name": user_name})
    if user:
        # Check if the user has a portfolio
        if "portfolio" in user:
            portfolio = user["portfolio"]
            stocks = portfolio.get("stocks", [])
            
            # Add the stock to the user's portfolio
            if stock_name not in stocks:
                stocks.append(stock_name)
                db.users.update_one(
                    {"user_name": user_name},
                    {"$set": {"portfolio.stocks": stocks}}
                )
                print(f"Stock '{stock_name}' added successfully.")
            else:
                print(f"Stock '{stock_name}' already exists in the portfolio.")
        else:
            print("User does not have a portfolio.")
    else:
        print("User not found.")

def delete_stock(db, user_name, stock_name):
    user = db.users.find_one({"user_name": user_name})
    if user:
        # Check if the user has a portfolio
        if "portfolio" in user:
            portfolio = user["portfolio"]
            stocks = portfolio.get("stocks", [])
            
            # Remove the stock from the user's portfolio
            if stock_name in stocks:
                # find index of stock
                index = stocks.index(stock_name)
                stocks.remove(stock_name)
                db.users.update_one(
                    {"user_name": user_name},
                    {"$set": {"portfolio.stocks": stocks}}
                )
                # Update the investment split accordingly
                investment_split = portfolio.get("investment_split", [])
                if index < len(investment_split):
                    investment_split.pop(index)
                    db.users.update_one(
                        {"user_name": user_name},
                        {"$set": {"portfolio.investment_split": investment_split}}
                    )
                print(f"Stock '{stock_name}' deleted successfully.")
            else:
                print(f"Stock '{stock_name}' not found in the portfolio.")
        else:
            print("User does not have a portfolio.")
    else:
        print("User not found.")

def delete_portfolio(db, user_name):
    user = db.users.find_one({"user_name": user_name})
    if user:
        # Remove the portfolio from the user's document
        db.users.update_one(
            {"user_name": user_name},
            {"$unset": {"portfolio": ""}}
        )
        print("Portfolio deleted successfully.")
    else:
        print("User not found.")


def create_expected_expenses(db, user_name, expense_label, expense_amount, recurring=False):
    user = db.users.find_one({"user_name": user_name})
    if user:
        # Check if the user already has an expenses field
        if "expenses" not in user:
            db.users.update_one({"user_name": user_name}, {"$set": {"expenses": []}})
        
        # Create the new expense entry
        new_expense = {
            "expense_label": expense_label,
            "expense_amount": expense_amount, 
            "recurring": recurring
        }
        
        # Add the new expense to the user's expenses array
        db.users.update_one({"user_name": user_name}, {"$push": {"expenses": new_expense}})
        print("Expense added successfully.")
    else:
        print("User not found.")

def update_expected_expenses(db, user_name, expense_label, field_to_update, new_value):
    user = db.users.find_one({"user_name": user_name})
    if user:
        # Find the expense within the user's expenses
        expense = next((e for e in user.get("expenses", []) if e["expense_label"] == expense_label), None)
        
        if expense:
            # Prepare the update based on the field_to_update
            if field_to_update in expense:
                # Update the specified field
                db.users.update_one(
                    {"user_name": user_name, "expenses.expense_label": expense_label},
                    {"$set": {f"expenses.$.{field_to_update}": new_value}}
                )
                print(f"Expense '{expense_label}' updated successfully. {field_to_update} is now {new_value}.")
            else:
                print(f"Field '{field_to_update}' does not exist in the expense.")
        else:
            print(f"Expense with label '{expense_label}' not found.")
    else:
        print("User not found.")

def get_expected_expenses(db, user_name):
    user = db.users.find_one({"user_name": user_name})
    if user:
        # Retrieve the user's expenses
        expenses = user.get("expenses", [])
        if expenses:
            print("Expected expenses:")
            for expense in expenses:
                print(f"- {expense['expense_label']}: {expense}")
            return expenses
        else:
            print("No expenses found for the user.")
            return []
    else:
        print("User not found.")
        return []

def delete_expected_expenses(db, user_name, expense_label):
    user = db.users.find_one({"user_name": user_name})
    if user:
        # Remove the expense from the user's expenses array
        result = db.users.update_one(
            {"user_name": user_name},
            {"$pull": {"expenses": {"expense_label": expense_label}}}
        )
        
        if result.modified_count > 0:
            print(f"Expense '{expense_label}' deleted successfully.")
        else:
            print(f"Expense with label '{expense_label}' not found.")
    else:
        print("User not found.")

def create_goal(db, user_name, goal_name, goal_amount, goal_duration, goal_current_amount=0, weekly_contributions = 0):
    user = db.users.find_one({"user_name": user_name})
    if user:
        # Check if the user already has a goals field
        if "goals" not in user:
            db.users.update_one({"user_name": user_name}, {"$set": {"goals": []}})
        
        # Create the new goal entry
        new_goal = {
            "goal_name": goal_name,
            "goal_amount": goal_amount,
            "goal_duration": goal_duration,
            "goal_start_date": datetime.now().strftime("%Y-%m-%d"),
            "goal_end_date": (datetime.now() + timedelta(days=goal_duration)).strftime("%Y-%m-%d"),
            "goal_current_amount": goal_current_amount,
            "weekly_contributions": weekly_contributions
        }
        
        # Add the new goal to the user's goals array
        db.users.update_one({"user_name": user_name}, {"$push": {"goals": new_goal}})
        print("Goal added successfully.")
    else:
        print("User not found.")

def update_goal(db, user_name, goal_name, field_to_update, new_value):
    user = db.users.find_one({"user_name": user_name})
    if user:
        # Find the goal within the user's goals
        goal = next((g for g in user.get("goals", []) if g["goal_name"] == goal_name), None)
        
        if goal:
            # Prepare the update based on the field_to_update
            if field_to_update in goal:
                # Update the specified field
                db.users.update_one(
                    {"user_name": user_name, "goals.goal_name": goal_name},
                    {"$set": {f"goals.$.{field_to_update}": new_value}}
                )
                print(f"Goal '{goal_name}' updated successfully. {field_to_update} is now {new_value}.")
            else:
                print(f"Field '{field_to_update}' does not exist in the goal.")
        else:
            print(f"Goal with name '{goal_name}' not found.")
    else:
        print("User not found.")

def delete_goal(db, user_name, goal_name):
    user = db.users.find_one({"user_name": user_name})
    if user:
        # Remove the goal from the user's goals array
        result = db.users.update_one(
            {"user_name": user_name},
            {"$pull": {"goals": {"goal_name": goal_name}}}
        )
        
        if result.modified_count > 0:
            print(f"Goal '{goal_name}' deleted successfully.")
        else:
            print(f"Goal with name '{goal_name}' not found.")
    else:
        print("User not found.")

def get_goals(db, user_name):
    user = db.users.find_one({"user_name": user_name})
    if user:
        # Retrieve the user's goals
        goals = user.get("goals", [])
        if goals:
            print("User's goals:")
            for goal in goals:
                print(f"- {goal['goal_name']}: {goal}")
            return goals
        else:
            print("No goals found for the user.")
            return []
    else:
        print("User not found.")
        return []


def preview_portfolio_add_stock(db, user_name, stock_name, stock_reduce, split_amount):
    """
    Previews the addition of a stock to the user's portfolio.
    
    Parameters:
    - db: Database connection object.
    - user_name (str): The ID of the user.
    - stock_name (str): The name of the stock to be added.
    - stock_amount (int): The amount of the stock to be added.
    
    Returns:
    - None
    """
    
    user = db.users.find_one({"user_name": user_name})
    if user:
        # Check if the user already has a stocks field
        if "stocks" not in user:
            db.users.update_one({"user_name": user_name}, {"$set": {"stocks": []}})
        
        # Create the new stock entry
        stocks = user.get("stocks", [])
        stocks.append(stock_name)
        investment_split = user.get("investment_split", [])
        
        # reduce investment split for stock_reduce by split_amount
        for i in range(len(investment_split)):
            if investment_split[i] == stock_reduce:
                investment_split[i] -= split_amount
                break
        investment_split.append(split_amount)


        # Preview the new stock entry
        # print(f"Previewing addition of stock: {stock_name}")
        
        # Calculate the expected return and risk of the portfolio with the new stock using investment_split and pc calc
        risk, return_rate = pc.calculate_portfolio_performance(stocks, investment_split)

        return risk, return_rate



    else:
        print("User not found.")

def get_stock_portfolio(db, user_name):
    """
    Retrieve the stock portfolio of a user.

    Parameters:
    - db: Database connection object.
    - user_name (str): The ID of the user.

    Returns:
    - portfolio (dict): The user's stock portfolio, or None if not found.
    """
    user = db.users.find_one({"user_name": user_name})
    if user:
        # Retrieve the user's portfolio
        portfolio = user.get("portfolio", {})
        if portfolio and "stocks" in portfolio:
            print("User's stock portfolio:")
            for stock, split in portfolio["stocks"].items():
                print(f"- {stock}: {split}%")
            return portfolio["stocks"]
        else:
            print("No stock portfolio found for the user.")
            return {}
    else:
        print("User not found.")
        return None

# def overall_investments_risk(db, user_name):
#     """
#     Calculate the overall risk of the user's investments.
    
#     Parameters:
#     - db: Database connection object.
#     - user_name (str): The ID of the user.
    
#     Returns:
#     - overall_risk (float): The overall risk of the user's investments including stock portfolio and fixed using weighted average based on split.
#     """
#     portfolio_risk = get()


# def create_portfolio(db, user_name, time_horizon, investment_amount, investment_split, stocks = []):
#     user = db.users.find_one({"user_name": user_name})
#     if user:
#         # Check if the user already has a portfolio field
#         if "portfolio" not in user:
#             db.users.update_one({"user_name": user_name}, {"$set": {"portfolio": []}})

#         if len(stocks) > 0:
#             # Get the risk and return rate from the portfolio_calcs module
#             risk, return_rate = pc.calculate_portfolio_performance(stocks, investment_split)
#         else:
#             risk = 0
#             return_rate = 0

#         # Create the new portfolio entry
#         new_portfolio = {
#             "stocks": stocks,
#             "risk": risk,
#             "return_rate": return_rate,
#             "time_horizon": time_horizon,
#             "investment_amount": investment_amount,
#             "investment_split": investment_split
#         }
        
#         # Add the new portfolio to the user's portfolio array
#         db.users.update_one({"user_name": user_name}, {"$push": {"portfolio": new_portfolio}})
#         print("Portfolio added successfully.")
#     else:
#         print("User not found.")

# def update_stock_portfolio(db, user_name, portfolio_name, field_to_update, new_value):
#     user = db.users.find_one({"user_name": user_name})
#     if user:
#         # Find the portfolio within the user's portfolios
#         portfolio = next((p for p in user.get("portfolio", []) if p["portfolio_name"] == portfolio_name), None)
        
#         if portfolio:
#             # Prepare the update based on the field_to_update
#             if field_to_update in portfolio:
#                 # Update the specified field
#                 # Check if the field is stocks
#                 if field_to_update == "stocks":
#                     # Get the risk and return rate from the portfolio_calcs module
#                     risk, return_rate = pc.calculate_portfolio_performance(new_value, portfolio["investment_split"])
#                     new_value = {
#                         "stocks": new_value,
#                         "risk": risk,
#                         "return_rate": return_rate
#                     }
#                 else:
#                     db.users.update_one(
#                         {"user_name": user_name, "portfolio.portfolio_name": portfolio_name},
#                         {"$set": {f"portfolio.$.{field_to_update}": new_value}}
#                     )
#                     print(f"Portfolio '{portfolio_name}' updated successfully. {field_to_update} is now {new_value}.")
#             else:
#                 print(f"Field '{field_to_update}' does not exist in the portfolio.")
#         else:
#             print(f"Portfolio with name '{portfolio_name}' not found.")


# def create_income(db, user_name, monthly_income):
#     # Find the user by user_name
#     user = db.users.find_one({"user_name": user_name})
    
#     # If user is found, update their monthly_income
#     if user:
#         db.users.update_one({"user_name": user_name}, {"$set": {"monthly_income": monthly_income}})
#         print("Monthly income updated successfully.")
#     else:
#         print("User not found.")

# def add_stock(db, user_name, stock_name, stock_amount):
#     user = db.users.find_one({"user_name": user_name})
#     if user:
#         # Check if the user already has a stocks field
#         if "stocks" not in user:
#             db.users.update_one({"user_name": user_name}, {"$set": {"stocks": []}})
        
#         # Create the new stock entry
#         new_stock = {
#             "stock_name": stock_name,
#             "stock_amount": stock_amount
#         }
        
#         # Add the new stock to the user's stocks array
#         db.users.update_one({"user_name": user_name}, {"$push": {"stocks": new_stock}})
#         print("Stock added successfully.")
#     else:
#         print("User not found.")