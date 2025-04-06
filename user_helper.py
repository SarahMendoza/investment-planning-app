
import calendar
import uuid
from datetime import datetime, timedelta

import portfolio_calcs as pc

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os

os.environ['MONGODB_PASS'] = 'pass'

if "MONGODB_PASS" in os.environ:
    uri = "mongodb+srv://sarahmendoza:HackSMU2024@cluster0.cmoki.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0".format(os.environ["MONGODB_PASS"])
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
        "age": age,
        "monthly_income": monthly_income
    }
    db.users.insert_one(user) 


def get_user_by_username(db, user_name):
    user = db.users.find_one({"user_name": user_name})
    if user:
        return {
            "user_name": user["user_name"],
            "first_name": user["first_name"],
            "last_name": user["last_name"],
            "email": user["email"],
            "password": user["password"],
            "age": user["age"],
            "monthly_income": user["monthly_income"]
        }
    else:
        return None

    

    




