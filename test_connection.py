

from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError

# Replace with your actual connection string
connection_string = "mongodb+srv://sarahmendoza:<HackSMU2024>@cluster0.cmoki.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

def test_connection():
    try:
        client = MongoClient(connection_string, serverSelectionTimeoutMS=5000)  # 5 seconds timeout
        client.admin.command('ping')  # Test the connection
        print("Connection successful!")
    except ServerSelectionTimeoutError as e:
        print("Connection failed:", e)
    except Exception as e:
        print("An error occurred:", e)

if __name__ == "__main__":
    test_connection()
