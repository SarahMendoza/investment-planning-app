
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
    userID = str(uuid.uuid4())
    #goalID = "123" 
    user = {
        "userID": userID,
        "user_name": user_name,
        "password": password,
        "age": age,
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "monthly_income": monthly_income
    }
    db.users.insert_one(user) 

def create_portfolio(db, userID, time_horizon, investment_amount, investment_split, stocks = []):
    user = db.users.find_one({"userID": userID})
    if user:
        # Check if the user already has a portfolio field
        if "portfolio" not in user:
            db.users.update_one({"userID": userID}, {"$set": {"portfolio": []}})

        if len(stocks) > 0:
            # Get the risk and return rate from the portfolio_calcs module
            risk, return_rate = pc.calculate_portfolio_performance(stocks, investment_split)
        else:
            risk = 0
            return_rate = 0

        # Create the new portfolio entry
        new_portfolio = {
            "stocks": stocks,
            "risk": risk,
            "return_rate": return_rate,
            "time_horizon": time_horizon,
            "investment_amount": investment_amount,
            "investment_split": investment_split
        }
        
        # Add the new portfolio to the user's portfolio array
        db.users.update_one({"userID": userID}, {"$push": {"portfolio": new_portfolio}})
        print("Portfolio added successfully.")
    else:
        print("User not found.")

def update_portfolio(db, userID, portfolio_name, field_to_update, new_value):
    user = db.users.find_one({"userID": userID})
    if user:
        # Find the portfolio within the user's portfolios
        portfolio = next((p for p in user.get("portfolio", []) if p["portfolio_name"] == portfolio_name), None)
        
        if portfolio:
            # Prepare the update based on the field_to_update
            if field_to_update in portfolio:
                # Update the specified field
                # Check if the field is stocks
                if field_to_update == "stocks":
                    # Get the risk and return rate from the portfolio_calcs module
                    risk, return_rate = pc.calculate_portfolio_performance(new_value, portfolio["investment_split"])
                    new_value = {
                        "stocks": new_value,
                        "risk": risk,
                        "return_rate": return_rate
                    }
                else:
                    db.users.update_one(
                        {"userID": userID, "portfolio.portfolio_name": portfolio_name},
                        {"$set": {f"portfolio.$.{field_to_update}": new_value}}
                    )
                    print(f"Portfolio '{portfolio_name}' updated successfully. {field_to_update} is now {new_value}.")
            else:
                print(f"Field '{field_to_update}' does not exist in the portfolio.")
        else:
            print(f"Portfolio with name '{portfolio_name}' not found.")


# def create_income(db, userID, monthly_income):
#     # Find the user by userID
#     user = db.users.find_one({"userID": userID})
    
#     # If user is found, update their monthly_income
#     if user:
#         db.users.update_one({"userID": userID}, {"$set": {"monthly_income": monthly_income}})
#         print("Monthly income updated successfully.")
#     else:
#         print("User not found.")

def create_expected_expenses(db, userID, expense_label, expense_amount, recurring=False):
    user = db.users.find_one({"userID": userID})
    if user:
        # Check if the user already has an expenses field
        if "expenses" not in user:
            db.users.update_one({"userID": userID}, {"$set": {"expenses": []}})
        
        # Create the new expense entry
        new_expense = {
            "expense_label": expense_label,
            "expense_amount": expense_amount, 
            "recurring": recurring
        }
        
        # Add the new expense to the user's expenses array
        db.users.update_one({"userID": userID}, {"$push": {"expenses": new_expense}})
        print("Expense added successfully.")
    else:
        print("User not found.")

def create_goal(db, userID, goal_name, goal_amount, goal_duration, goal_current_amount=0, weekly_contributions = 0):
    user = db.users.find_one({"userID": userID})
    if user:
        # Check if the user already has a goals field
        if "goals" not in user:
            db.users.update_one({"userID": userID}, {"$set": {"goals": []}})
        
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
        db.users.update_one({"userID": userID}, {"$push": {"goals": new_goal}})
        print("Goal added successfully.")
    else:
        print("User not found.")

def update_goal(db, userID, goal_name, field_to_update, new_value):
    user = db.users.find_one({"userID": userID})
    if user:
        # Find the goal within the user's goals
        goal = next((g for g in user.get("goals", []) if g["goal_name"] == goal_name), None)
        
        if goal:
            # Prepare the update based on the field_to_update
            if field_to_update in goal:
                # Update the specified field
                db.users.update_one(
                    {"userID": userID, "goals.goal_name": goal_name},
                    {"$set": {f"goals.$.{field_to_update}": new_value}}
                )
                print(f"Goal '{goal_name}' updated successfully. {field_to_update} is now {new_value}.")
            else:
                print(f"Field '{field_to_update}' does not exist in the goal.")
        else:
            print(f"Goal with name '{goal_name}' not found.")
    else:
        print("User not found.")

def delete_goal(db, userID, goal_name):
    user = db.users.find_one({"userID": userID})
    if user:
        # Remove the goal from the user's goals array
        result = db.users.update_one(
            {"userID": userID},
            {"$pull": {"goals": {"goal_name": goal_name}}}
        )
        
        if result.modified_count > 0:
            print(f"Goal '{goal_name}' deleted successfully.")
        else:
            print(f"Goal with name '{goal_name}' not found.")
    else:
        print("User not found.")

# def add_stock(db, userID, stock_name, stock_amount):
#     user = db.users.find_one({"userID": userID})
#     if user:
#         # Check if the user already has a stocks field
#         if "stocks" not in user:
#             db.users.update_one({"userID": userID}, {"$set": {"stocks": []}})
        
#         # Create the new stock entry
#         new_stock = {
#             "stock_name": stock_name,
#             "stock_amount": stock_amount
#         }
        
#         # Add the new stock to the user's stocks array
#         db.users.update_one({"userID": userID}, {"$push": {"stocks": new_stock}})
#         print("Stock added successfully.")
#     else:
#         print("User not found.")

