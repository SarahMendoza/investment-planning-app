
import calendar
import uuid
from datetime import datetime, timedelta

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os

os.environ['MONGODB_PASS'] = 'HackSMU2024'

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

#static functions for database operations

