
import calendar
import uuid
from datetime import datetime, timedelta

import portfolio_calcs as pc

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os

os.environ['MONGODB_PASS'] = 'pass'

if "MONGODB_PASS" in os.environ:
    uri = "mongodb+srv://mongo uri here".format(os.environ["MONGODB_PASS"])
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

API_KEY = 'generate key for model'
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
    dob = datetime.strptime(dob_string, "%m-%d-%Y")

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
        # Only update if portfolio exists, otherwise create one
        if "portfolio" in user:
            print("User already has a portfolio. Updating the existing portfolio.")
        else:
            print("Creating new portfolio for the user.")
        
        # Calculate risk and return rate if stocks are provided
        risk, return_rate = pc.calculate_portfolio_performance(stocks, investment_split) if stocks else (0, 0)

        updated_portfolio = {
            "stocks": stocks,
            "risk": risk,
            "return_rate": return_rate,
            "time_horizon": time_horizon,
            "investment_amount": investment_amount,
            "investment_split": investment_split
        }

        # Update the portfolio (or create a new one if it doesn't exist)
        db.users.update_one(
            {"user_name": user_name},
            {"$set": {"portfolio": updated_portfolio}}
        )
        print("Portfolio updated/created successfully.")
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

# def add_stock(db, user_name, stock_name, investment_amount):
#     user = db.users.find_one({"user_name": user_name})
#     if user:
#         # Check if the user has a portfolio
#         if "portfolio" in user:
#             portfolio = user["portfolio"]
#             stocks = portfolio.get("stocks", [])
            
#             # Add the stock to the user's portfolio
#             if stock_name not in stocks:
#                 stocks.append(stock_name)
#                 investment_amounts = portfolio["investment_amount"] * portfolio["investment_split"]
#                 # investment_split = investment_amounts/portfolio["investment_amount"]
#                 investment_split = [x / portfolio["investment_amount"] for x in investment_amounts]
#                 portfolio["investment_amount"] += investment_amount
#                 # Update the investment split accordingly
#                 investment_split.append(investment_amount/portfolio["investment_amount"])

                
#                 # find total invesment amount for current portfolio
#                 total_investment = sum(investment_split)
#                 db.users.update_one(
#                     {"user_name": user_name},
#                     {"$set": {"portfolio.stocks": stocks}},
#                     {"$set": {"portfolio.investment_split": investment_split}},
#                     {"$set": {"portfolio.investment_amount": total_investment}}
#                 )
#                 #print(f"Stock '{stock_name}' added successfully.")
#             else:
#                 print(f"Stock '{stock_name}' already exists in the portfolio.")
#         else:
#             print("User does not have a portfolio.")
#     else:
#         print("User not found.")

def add_stock(db, user_name, stock_name, investment_amount):
    user = db.users.find_one({"user_name": user_name})
    if user:
        # Check if the user has a portfolio
        if "portfolio" in user:
            portfolio = user["portfolio"]
            stocks = portfolio.get("stocks", [])
            investment_amounts = portfolio.get("investment_amounts", [])  # list for each stock's investment amount
            investment_splits = portfolio.get("investment_splits", [])  # list for each stock's investment split
            
            # Add the stock to the user's portfolio
            if stock_name not in stocks:
                # Append the new stock and its associated investment amount and split
                stocks.append(stock_name)
                investment_amounts.append(investment_amount)
                # Calculate the new investment split for this stock
                total_investment = sum(investment_amounts)
                investment_splits = [amount / total_investment for amount in investment_amounts]

                # Update the user's portfolio with the new data
                db.users.update_one(
                    {"user_name": user_name},
                    {"$set": {
                        "portfolio.stocks": stocks,
                        "portfolio.investment_amounts": investment_amounts,
                        "portfolio.investment_splits": investment_splits,
                        "portfolio.investment_amount": total_investment
                    }}
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
            "goal_start_date": datetime.now().strftime("%m-%d-%Y"),
            "goal_end_date": (datetime.now() + timedelta(days=goal_duration)).strftime("%m-%d-%Y"),
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
            # also get the risk and return rate
            risk = portfolio.get("risk")
            return_rate = portfolio.get("return_rate")
            # print("User's stock portfolio:")
            # for stock, split in portfolio["stocks"].items():
            #     print(f"- {stock}: {split}%")
            return portfolio["stocks"], risk, return_rate
        else:
            print("No stock portfolio found for the user.")
            return {}
    else:
        print("User not found.")
        return None

def add_fixed_investment(db, user_name, investment_name, investment_amount, investment_duration, interest_rate, start_date, end_date, risk, return_rate):
    user = db.users.find_one({"user_name": user_name})
    if user:
        # Check if the user already has an expenses field
        if "expenses" not in user:
            db.users.update_one({"user_name": user_name}, {"$set": {"expenses": []}})
        
        # Create the new expense entry
        new_investment = {
        "investment_name": investment_name,
        "investment_amount": investment_amount,
        "investment_duration": investment_duration,
        "interest_rate": interest_rate,
        "start_date": start_date,
        "end_date": end_date,
        "risk": risk,
        "return_rate": return_rate
    }
        
        # Add the new expense to the user's expenses array
        db.users.update_one({"user_name": user_name}, {"$push": {"fixed_investments": new_investment}})
        print("Expense added successfully.")
    else:
        print("User not found.")


def create_fixed_investment(db, user_name, investment_name, investment_amount, investment_duration, risk, return_rate):
    user = db.users.find_one({"user_name": user_name})
    
    if user:
        # Check if the user has a portfolio
        # if "portfolio" in user:
            # portfolio = user["portfolio"]
            # investments = portfolio.get("fixed_investments", [])
            
            # Add new fixed investment to the list
            new_investment = {
                "investment_name": investment_name,
                "investment_amount": investment_amount,
                "investment_duration": investment_duration,
                "risk": risk,
                "return_rate": return_rate
            }
            # investments.append(new_investment)
            
            # Update the user's fixed investments
            db.users.update_one(
                {"user_name": user_name},
                {"$push": {"fixed_investments": [new_investment]}}
            )
            print(f"Fixed investment '{investment_name}' added successfully.")
        # else:
        #     print("User does not have a portfolio.")
    else:
        print("User not found.")

def overall_investments_risk(db, user_name):
    """
    Calculate the overall risk of the user's investments.
    
    Parameters:
    - db: Database connection object.
    - user_name (str): The ID of the user.
    
    Returns:
    - overall_risk (float): The overall risk of the user's investments, including stock portfolio and fixed investments, weighted by investment amounts.
    """
    # Retrieve stocks and their associated risks
    stocks, stock_risks, stock_amounts = get_stock_portfolio(db, user_name)

    # Debugging: Validate if stock data is properly fetched
    if not stocks or stock_amounts is None or not stock_risks:
        print(f"Error: Invalid stock data for user '{user_name}'. Stocks: {stocks}, Amounts: {stock_amounts}, Risks: {stock_risks}")
        return 0
    
    # Find the user in the database
    user = db.users.find_one({"user_name": user_name})
    if user:
        # Retrieve the user's fixed investments
        fixed_investments = user.get("portfolio", {}).get("fixed_investments", [])
        
        # Initialize variables for total risk and total amount
        total_fixed_risk = 0
        total_fixed_amount = 0
        fixed_total_risk = 0
        
        # Debugging: Print fixed investments data
        print(f"Fixed investments for user '{user_name}': {fixed_investments}")
        
        if fixed_investments:
            # Calculate the total risk and amount for fixed investments
            total_fixed_amount = sum(investment["investment_amount"] for investment in fixed_investments)
            print(f"Total fixed amount: {total_fixed_amount}")
            
            for investment in fixed_investments:
                if investment.get("risk") is None:
                    print(f"Warning: Missing risk for investment: {investment}")
                    continue  # Skip if risk is missing
                fixed_investment_risk = investment["risk"] * (investment["investment_amount"] / total_fixed_amount)
                total_fixed_risk += fixed_investment_risk
            print(f"Total fixed risk: {total_fixed_risk}")
        else:
            print("No fixed investments found for the user.")
            total_fixed_risk = 0  # Assign default risk value if no fixed investments

        # Initialize variables for stocks if available
        total_stock_risk = 0
        total_stock_amount = sum(stock_amounts)
        print(f"Total stock amount: {total_stock_amount}")
        
        if stocks:
            # Calculate the total risk for stocks based on their amounts
            for i, stock in enumerate(stocks):
                if stock_risks[i] is None:
                    print(f"Warning: Missing risk for stock: {stock}")
                    continue  # Skip if risk is missing
                stock_risk = stock_risks[i] * (stock_amounts[i] / total_stock_amount)
                total_stock_risk += stock_risk
            print(f"Total stock risk: {total_stock_risk}")
        else:
            print("No stocks found for the user.")
        
        # If no investments at all, just return 0
        if total_fixed_amount == 0 and total_stock_amount == 0:
            print(f"No investments found for user '{user_name}'. Returning risk of 0.")
            return 0
        
        # Calculate the overall weighted risk of the portfolio
        total_amount = total_fixed_amount + total_stock_amount
        print(f"Total amount (fixed + stocks): {total_amount}")
        
        total_risk = (total_fixed_risk * total_fixed_amount + total_stock_risk * total_stock_amount) / total_amount
        print(f"Calculated total risk: {total_risk}")
        
        return total_risk
    else:
        print(f"User '{user_name}' not found.")
        return 0


def get_fixed_investments(db, user_name):
    """
    Retrieve the fixed investments of a user.

    Parameters:
    - db: Database connection object.
    - user_name (str): The ID of the user.

    Returns:
    - fixed_investments (list): The user's fixed investments, or None if not found.
    """
    user = db.users.find_one({"user_name": user_name})
    if user:
        # Retrieve the user's fixed investments
        fixed_investments = user.get("fixed_investments", [])
        if fixed_investments:
            print("User's fixed investments:")
            for investment in fixed_investments:
                print(f"- {investment['investment_name']}: {investment}")
            return fixed_investments
        else:
            print("No fixed investments found for the user.")
            return []
    else:
        print("User not found.")
        return None
    
def overall_investments_risk(db, user_name):
    """
    Calculate the overall risk and return of the user's investments.
    
    Parameters:
    - db: Database connection object.
    - user_name (str): The ID of the user.
    
    Returns:
    - overall_risk (float): The overall risk of the user's investments.
    - overall_return (float): The overall return of the user's investments.
    """
    stocks, stock_risks, stock_amounts = get_stock_portfolio(db, user_name)
    
    # Find the user in the database
    user = db.users.find_one({"user_name": user_name})
    if user:
        # Retrieve the user's fixed investments
        fixed_investments = user.get("portfolio", {}).get("fixed_investments", [])
        
        # Initialize variables for total risk and total amount
        total_fixed_risk = 0
        total_fixed_amount = 0
        fixed_total_risk = 0
        
        if fixed_investments:
            # Calculate the total risk and amount for fixed investments
            total_fixed_amount = sum(investment["investment_amount"] for investment in fixed_investments)
            
            for investment in fixed_investments:
                if investment.get("risk") is None:
                    continue  # Skip if risk is missing
                fixed_investment_risk = investment["risk"] * (investment["investment_amount"] / total_fixed_amount)
                total_fixed_risk += fixed_investment_risk

        # Initialize variables for stocks if available
        total_stock_risk = 0
        total_stock_amount = sum(stock_amounts)
        
        if stocks:
            # Calculate the total risk for stocks based on their amounts
            for i, stock in enumerate(stocks):
                if stock_risks[i] is None:
                    continue  # Skip if risk is missing
                stock_risk = stock_risks[i] * (stock_amounts[i] / total_stock_amount)
                total_stock_risk += stock_risk

        # If no investments at all, just return 0
        if total_fixed_amount == 0 and total_stock_amount == 0:
            return 0, 0
        
        # Calculate the overall weighted risk of the portfolio
        total_amount = total_fixed_amount + total_stock_amount
        
        overall_risk = (total_fixed_risk * total_fixed_amount + total_stock_risk * total_stock_amount) / total_amount
        
        # Calculate overall
        overall_return = (total_fixed_amount * sum(investment["return_rate"] for investment in fixed_investments) + total_stock_amount * sum(stock_risks)) / total_amount
        return overall_risk, overall_return

# def create_fixed_investment(db, user_name, investment_name, investment_amount, investment_duration, ticker, start_date, end_date, interest_rate=None, investment_type='fixed_income', investment_category=None):
#     """
#     Create a fixed investment record in the database (MongoDB) and include risk and return rate.
    
#     Args:
#         db (MongoDB database connection): The MongoDB database to store the investment data.
#         user_name (str): The name of the user making the investment.
#         investment_name (str): The name of the investment (e.g., "Bonds").
#         investment_amount (float): The total amount invested.
#         investment_duration (int): Duration of the investment (e.g., 5 years).
#         ticker (str): Ticker symbol of the asset (e.g., 'AAPL').
#         start_date (str): The start date of the investment in 'YYYY-MM-DD' format.
#         end_date (str): The end date of the investment in 'YYYY-MM-DD' format.
#         interest_rate (float, optional): The rate of return or interest rate (if applicable).
#         investment_type (str, optional): The type of investment, default is 'fixed_income'.
#         investment_category (str, optional): Category of the investment, e.g., 'Bonds', 'Stocks', etc.
        
#     Returns:
#         dict: The created investment object with a MongoDB ObjectID.
#     """
#     # Calculate the risk and return rate for the asset
#     risk, return_rate = pc.calculate_risk_and_return(ticker, start_date, end_date)

#     # Prepare the document to insert into MongoDB
#     investment = {
#         'user_name': user_name,
#         'investment_name': investment_name,
#         'investment_amount': investment_amount,
#         'investment_duration': investment_duration,
#         'interest_rate': interest_rate if interest_rate else None,  # Optional field
#         'start_date': start_date,
#         'end_date': end_date,
#         'investment_type': investment_type,
#         'investment_category': investment_category if investment_category else None,  # Optional field
#         'risk': risk,  # Add the calculated risk (volatility)
#         'return_rate': return_rate,  # Add the calculated return rate
#         'date_created': datetime.now()  # Add the creation timestamp
#     }

    # Insert the investment document into MongoDB
    # result = db.fixed_investments.insert_one(investment)
    
    # Return the inserted investment document with its MongoDB ObjectId
    # return {
    #     'investment_id': str(result.inserted_id),
    #     'investment_data': investment
    # }

    # Define the new investment to add
    
    # # get all current fixed investments if they exist
    # user = db.users.find_one({"user_name": user_name})
    # if user:
    #     # Check if the user already has a fixed investments field
    #     if "fixed_investments" not in user:
    #         db.users.update_one({"user_name": user_name}, {"$set": {"fixed_investments": []}})
        
    #     # Add the new investment to the user's fixed investments array
    #     db.users.update_one({"user_name": user_name}, {"$push": {"fixed_investments": new_investment}})
    #     print("Fixed investment added successfully.")
    # else:
    #     print("User not found.")
    
    # add new investment to fixed investments

    
    # # Find the user and ensure the portfolio exists, then push the new investment
    # result = db.users.update_one(
    #     {"user_name": user_name},
    #     {
    #         {"$set": {"fixed_investment": fixed_investment}}
    #     },
    #     upsert=True  # Creates the user document if it doesn't exist
    # )
    
    # Check if the user was found or created
    # if result.matched_count == 0 and result.upserted_id is None:
    #     return {"error": "User not found or unable to create."}

    # # Confirm the update
    # return {"message": f"Fixed investment '{investment_name}' added successfully to {user_name}'s portfolio."}


# def overall_investments_risk(db, user_name):
#     """
#     Calculate the overall risk of the user's investments.
    
#     Parameters:
#     - db: Database connection object.
#     - user_name (str): The ID of the user.
    
#     Returns:
#     - overall_risk (float): The overall risk of the user's investments including stock portfolio and fixed using weighted average based on split.
#     """
#     stocks, risk, return_rate = get_stock_portfolio(db, user_name)
#     # find all fixed investments for user
#     user = db.users.find_one({"user_name": user_name})
#     if user:
#         # Retrieve the user's fixed investments
#         fixed_investments = user.get("portfolio", {}).get("fixed_investments", [])
#         if fixed_investments:
#             # Calculate the overall risk of fixed investments
#             total_fixed_risk = sum(investment["risk"] for investment in fixed_investments)
#             total_fixed_amount = sum(investment["investment_amount"] for investment in fixed_investments)

#             # Calculate the weighted average risk of fixed investments
#             for investment in fixed_investments:
#                 investment["risk"] = investment["risk"] * (investment["investment_amount"] / total_fixed_amount)
            
#             fixed_total_risk = sum(investment["risk"])
#         else:
#             print("No fixed investments found for the user.")
#             return 0

#         # Calculate the overall risk of stocks
#         if stocks:
#             # Calculate the risk of stocks based on the investment split
#             total_stock_amount = sum(investment["investment_amount"] for investment in stocks)
#             # Calculate the weighted average risk of stocks
#             for investment in stocks:
#                 investment["risk"] = investment["risk"] * (investment["investment_amount"] / total_stock_amount)
#             stock_total_risk = sum(investment["risk"])
#         else:
#             print("No stocks found for the user.")
#             return 0

#         # Calculate the overall weighted risk of the portfolio
#         if stocks and fixed_investments:
#             total_amount = total_fixed_amount + sum(investment["investment_amount"] for investment in stocks)
#             total_risk = (fixed_total_risk * total_fixed_amount + stock_total_risk * sum(investment["investment_amount"] for investment in stocks)) / total_amount

#             # Combine the risks using a weighted average based on investment amounts
#         return total_risk
#         # fixed_investment_weight = total_fixed_amount / (total_fixed_amount + sum(investment["investment_amount"] for investment in stocks))
#         # stock_weight = sum(investment["investment_amount"] for investment in stocks) / (total_fixed_amount + sum(investment["investment_amount"] for investment in stocks))
#         # overall_risk = (fixed_investment_weight * total_fixed_risk + stock_weight * risk) / (fixed_investment_weight + stock_weight)
#         # return overall_risk
#     else:
#         print("User not found.")
#         return 0


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
