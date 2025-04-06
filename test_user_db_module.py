import unittest
from pymongo import MongoClient
from datetime import datetime, timedelta
from user_db_module import create_user, get_user, update_user, delete_user, create_portfolio, update_stock_portfolio, add_stock, delete_stock, create_goal, get_goals

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

    def test_update_user(self):
        # Test updating a user field
        self.db.users.insert_one(self.user_data)
        
        update_user(self.db, "johndoe", "monthly_income", 3500)
        
        user = self.db.users.find_one({"user_name": "johndoe"})
        self.assertEqual(user["monthly_income"], 3500)

    def test_delete_user(self):
        # Test deleting a user
        self.db.users.insert_one(self.user_data)
        
        delete_user(self.db, "johndoe")
        
        user = self.db.users.find_one({"user_name": "johndoe"})
        self.assertIsNone(user)

    def test_create_portfolio(self):
        # Test creating a portfolio
        self.db.users.insert_one(self.user_data)
        
        create_portfolio(self.db, "johndoe", 5, 10000, [50, 50], ["AAPL", "GOOG"])
        
        user = self.db.users.find_one({"user_name": "johndoe"})
        self.assertIn("portfolio", user)
        self.assertEqual(user["portfolio"]["stocks"], ["AAPL", "GOOG"])

    def test_update_stock_portfolio(self):
        # Test updating stock portfolio
        self.db.users.insert_one(self.user_data)
        create_portfolio(self.db, "johndoe", 5, 10000, [50, 50], ["AAPL", "GOOG"])
        
        update_stock_portfolio(self.db, "johndoe", "investment_split", [60, 40])
        
        user = self.db.users.find_one({"user_name": "johndoe"})
        self.assertEqual(user["portfolio"]["investment_split"], [60, 40])

    def test_add_stock(self):
        # Test adding a stock to the portfolio
        self.db.users.insert_one(self.user_data)
        create_portfolio(self.db, "johndoe", 5, 10000, [50, 50], ["AAPL", "GOOG"])
        
        add_stock(self.db, "johndoe", "MSFT", 50)
        
        user = self.db.users.find_one({"user_name": "johndoe"})
        self.assertIn("MSFT", user["portfolio"]["stocks"])

    def test_delete_stock(self):
        # Test deleting a stock from the portfolio
        self.db.users.insert_one(self.user_data)
        create_portfolio(self.db, "johndoe", 5, 10000, [50, 50], ["AAPL", "GOOG"])
        
        delete_stock(self.db, "johndoe", "GOOG")
        
        user = self.db.users.find_one({"user_name": "johndoe"})
        self.assertNotIn("GOOG", user["portfolio"]["stocks"])

    def test_create_goal(self):
        # Test creating a goal
        self.db.users.insert_one(self.user_data)
        
        create_goal(self.db, "johndoe", "Buy a house", 50000, 365, 10000, 500)
        
        user = self.db.users.find_one({"user_name": "johndoe"})
        self.assertIn("goals", user)
        self.assertEqual(len(user["goals"]), 1)
        self.assertEqual(user["goals"][0]["goal_name"], "Buy a house")

    def test_get_goals(self):
        # Test retrieving goals for a user
        self.db.users.insert_one(self.user_data)
        create_goal(self.db, "johndoe", "Buy a house", 50000, 365, 10000, 500)
        
        goals = get_goals(self.db, "johndoe")
        self.assertEqual(len(goals), 1)
        self.assertEqual(goals[0]["goal_name"], "Buy a house")

if __name__ == "__main__":
    unittest.main()
