import unittest
from pymongo import MongoClient
from datetime import datetime, timedelta
from user_db_module import create_fixed_investment, overall_investments_risk, add_fixed_investment, create_user, get_user, update_user, delete_user, create_portfolio, update_stock_portfolio, add_stock, delete_stock, create_goal, get_goals, get_fixed_investments

class TestUserPortfolioFunctions(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Connect to MongoDB (use a real instance or MongoDB Atlas)
        cls.client = MongoClient("mongodb+srv://sarahmendoza:HackSMU2024@cluster0.cmoki.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")  # Replace with your MongoDB URI
        cls.db = cls.client.test_database  # Use a test database (it will be created if it doesn't exist)
        
        # Make sure the collection is empty before running tests
        cls.db.users.drop()

    @classmethod
    def tearDownClass(cls):
        # Clean up by dropping the test database after tests
        cls.db.users.drop()
        cls.client.close()

    def setUp(self):
        # Prepare some common test data
        self.user_data = {
            "user_name": "johndoe",
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "password": "password123",
            "dob": "01-01-1901",
            "monthly_income": 3000
        }

    def test_create_user(self):
        # Test creating a user
        create_user(self.db, "johndoe", "John", "Doe", "john.doe@example.com", "password123", "01-01-1901", 3000)
        user = self.db.users.find_one({"user_name": "johndoe"})
        
        self.assertIsNotNone(user)
        self.assertEqual(user["user_name"], "johndoe")
        self.assertEqual(user["first_name"], "John")
        self.assertEqual(user["last_name"], "Doe")
        self.assertEqual(user["email"], "john.doe@example.com")

    def test_get_user(self):
        # Test retrieving a user
        self.db.users.insert_one(self.user_data)
        
        user = get_user(self.db, "johndoe")
        
        self.assertEqual(user["user_name"], "johndoe")
        self.assertEqual(user["first_name"], "John")

    # def test_update_user(self):
    #     # Test updating a user field
    #     self.db.users.insert_one(self.user_data)
        
    #     update_user(self.db, "johndoe", "monthly_income", 3500)
        
    #     user = self.db.users.find_one({"user_name": "johndoe"})
    #     self.assertEqual(user["monthly_income"], 3500)

    # # def test_delete_user(self):
    # #     # Test deleting a user
    # #     self.db.users.insert_one(self.user_data)
        
    # #     delete_user(self.db, "johndoe")
        
    # #     user = self.db.users.find_one({"user_name": "johndoe"})
    # #     self.assertIsNone(user)

    # def test_create_portfolio(self):
    #     # Test creating a portfolio
    #     self.db.users.insert_one(self.user_data)
        
    #     create_portfolio(self.db, "johndoe", 5, 10000, [50, 50], ["AAPL", "GOOG"])
        
    #     user = self.db.users.find_one({"user_name": "johndoe"})
    #     self.assertIn("portfolio", user)
    #     self.assertEqual(user["portfolio"]["stocks"], ["AAPL", "GOOG"])

    # def test_update_stock_portfolio(self):
    #     # Test updating stock portfolio
    #     self.db.users.insert_one(self.user_data)
    #     create_portfolio(self.db, "johndoe", 5, 10000, [50, 50], ["AAPL", "GOOG"])
        
    #     update_stock_portfolio(self.db, "johndoe", "investment_split", [60, 40])
        
    #     user = self.db.users.find_one({"user_name": "johndoe"})
    #     self.assertEqual(user["portfolio"]["investment_split"], [60, 40])

    # def test_add_stock(self):
    #     # Test adding a stock to the portfolio
    #     self.db.users.insert_one(self.user_data)
    #     create_portfolio(self.db, "johndoe", 5, 10000, [50, 50], ["AAPL", "GOOG"])
        
    #     add_stock(self.db, "johndoe", "MSFT", 50)
        
    #     user = self.db.users.find_one({"user_name": "johndoe"})
    #     self.assertIn("MSFT", user["portfolio"]["stocks"])

    # def test_delete_stock(self):
    #     # Test deleting a stock from the portfolio
    #     self.db.users.insert_one(self.user_data)
    #     create_portfolio(self.db, "johndoe", 5, 10000, [50, 50], ["AAPL", "GOOG"])
        
    #     delete_stock(self.db, "johndoe", "GOOG")
        
    #     user = self.db.users.find_one({"user_name": "johndoe"})
    #     self.assertNotIn("GOOG", user["portfolio"]["stocks"])

    # def test_create_goal(self):
    #     # Test creating a goal
    #     self.db.users.insert_one(self.user_data)
        
    #     create_goal(self.db, "johndoe", "Buy a house", 50000, 365, 10000, 500)
        
    #     user = self.db.users.find_one({"user_name": "johndoe"})
    #     self.assertIn("goals", user)
    #     self.assertEqual(len(user["goals"]), 1)
    #     self.assertEqual(user["goals"][0]["goal_name"], "Buy a house")

    def test_get_goals(self):
        # Test retrieving goals for a user
        self.db.users.insert_one(self.user_data)
        create_goal(self.db, "johndoe", "Buy a house", 50000, 365, 10000, 500)
        goals = get_goals(self.db, "johndoe")

        #print(goals)
        self.assertEqual(len(goals), 1)
        self.assertEqual(goals[0]["goal_name"], "Buy a house")

    # def test_add_fixed_investment(self):
    #     # Test adding a fixed investment to a user's portfolio
    #     investment_name = "Bonds"
    #     investment_amount = 5000
    #     investment_duration = 5  # years
    #     interest_rate = 4.5  # percent
    #     start_date = "2023-01-01"
    #     end_date = "2028-01-01"
    #     risk = 0.02  # assumed risk factor
    #     return_rate = 0.05  # assumed return rate
        
    #     # Call the function to add the fixed investment
    #     result = add_fixed_investment(self.db, "johndoe", investment_name, investment_amount, investment_duration,
    #                                   interest_rate, start_date, end_date, risk, return_rate)
        
    #     # Retrieve the user and check if the investment is added
    #     user = self.db.users.find_one({"user_name": "johndoe"})
    #     investments = get_fixed_investments(user, "johndoe")
        
    #     self.assertEqual(result["message"], f"Fixed investment '{investment_name}' added successfully to johndoe's portfolio.")
    #     self.assertEqual(len(investments), 1)
    #     self.assertEqual(investments[0]["investment_name"], investment_name)
    #     self.assertEqual(investments[0]["investment_amount"], investment_amount)

    # def test_create_fixed_investment(self):
    #     # Test creating a fixed investment directly (without the 'add' method)
    #     investment_name = "Bonds"
    #     investment_amount = 5000
    #     investment_duration = 5  # years
    #     risk = 0.02  # assumed risk factor
    #     return_rate = 0.05  # assumed return rate
        
    #     # Call the function to create the fixed investment
    #     create_fixed_investment(self.db, "johndoe", investment_name, investment_amount, investment_duration, risk, return_rate)
        
    #     # Retrieve the user and check if the investment is created
    #     user = self.db.user_name.find_one({"user_name": "johndoe"})
    #     investments = user["fixed_investments"]
        
    #     self.assertEqual(len(investments), 1)
    #     self.assertEqual(investments[0]["investment_name"], investment_name)
    #     self.assertEqual(investments[0]["investment_amount"], investment_amount)

    # def test_overall_investments_risk(self):
    #     # Test calculating the overall risk of the user's investments (including both fixed and stock investments)
    #     investment_name = "Bonds"
    #     investment_amount = 5000
    #     investment_duration = 5  # years
    #     interest_rate = 4.5  # percent
    #     start_date = "01-01-2023"
    #     end_date = "01-01-2028"
    #     risk = 0.02  # assumed risk factor for fixed investments
    #     return_rate = 0.05  # assumed return rate for fixed investments
        
    #     # Add a fixed investment
    #     add_fixed_investment(self.db, "johndoe", investment_name, investment_amount, investment_duration,
    #                          interest_rate, start_date, end_date, risk, return_rate)
        
    #     # Assuming you have some stock investments (you can manually insert them here)
    #     stock_investments = [
    #         {"investment_name": "AAPL", "investment_amount": 10000, "risk": 0.03, "return_rate": 0.07},
    #         {"investment_name": "GOOG", "investment_amount": 15000, "risk": 0.02, "return_rate": 0.06}
    #     ]
    #     self.db.users.update_one(
    #         {"user_name": "johndoe"},
    #         {"$set": {"portfolio.stocks": stock_investments}}
    #     )

    #     # Calculate the overall risk of the investments
    #     total_risk, returns = overall_investments_risk(self.db, "johndoe")
        
    #     # Check that the overall risk is calculated correctly (this is a placeholder, adjust as necessary)
    #     self.assertGreater(total_risk, returns)  # It should be a positive value since we have investments

# if __name__ == "__main__":
#     unittest.main()
if __name__ == "__main__":
    unittest.main()
