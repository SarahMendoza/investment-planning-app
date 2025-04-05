import jwt
import datetime
from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'PLZ'  # Replace with your secret key

# Function to generate JWT token
def generate_token():
    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1),  # Expiration time (1 hour)
        'iat': datetime.datetime.utcnow(),  # Issued at time
        'sub': 'user_id'  # Subject (this could be the user ID or username)
    }
    return jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')

# For testing, generate a token and print it
if __name__ == "__main__":
    token = generate_token()
    print(f"Generated Token: {token}")
