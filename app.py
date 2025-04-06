# file for storing 


import yfinance as yf
from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import user_helper

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return 'Flask is running!'

@app.route('/api/stock-list', methods=['POST'])
def get_stock_list_data():
    print("Received request to /api/stock-list")
    data = request.get_json()
    print("Request JSON:", data)
    
    ticker_list = data.get('ticker_list', [])
    print("Tickers:", ticker_list)

    data_list = []
    for ticker in ticker_list:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="1mo")
        info = stock.info

        current_data = {
            'ticker': ticker,
            'history': hist.to_dict(orient='records'),
            'info': info
        }
        data_list.append(current_data)

    return jsonify(data_list)


#############################################
# APIs for authentication & user operations #
#############################################

#validate unique username and create user
@app.route('/user/create', methods=['POST'])
def unique_username():
    data = request.get_json()
    print("Received user creation request:", data)

    # query the database to check if the username already exists
    user = user_helper.get_user_by_username(user_helper.db, data['user_name'])
    if user:
        return jsonify({"error": "Username already exists"}), 409
    else:
        # If the username is unique, proceed with user creation
        user_helper.create_user(
            user_helper.db,
            data['user_name'],
            data['first_name'],
            data['last_name'],
            data['email'],
            data['password'],
            data['dob'],
            data['monthly_income']
        )
        print("User created successfully!")

    
    return jsonify({"message": "User created successfully!"}), 201

# #create a new user
# @app.route('/user/create', methods=['POST'])
# def create_user():

#     try:
#         data = request.get_json()
#         print("Received user creation request:", data)

#         user_helper.create_user(
#             user_helper.db,
#             data['user_name'],
#             data['first_name'],
#             data['last_name'],
#             data['email'],
#             data['password'],
#             data['dob'],
#             data.get('monthly_income', 0)
#         )
#         return jsonify({"message": "User created successfully!"}), 201
#     except Exception as e:
#         print("Error creating user:", e)
#         return jsonify({"error": "Failed to create user"}), 500


#login user
@app.route('/user/login', methods=['POST'])
def login_user():
    data = request.get_json()
    print("Received login request:", data)

    # query the database to check if the username already exists
    user = user_helper.get_user_by_username(user_helper.db, data['user_name'])
    
    if not user:
        return jsonify({"error": "User not found"}), 404
        

    if user['password'] != data['password']:
        return jsonify({"error": "Invalid password"}), 401

    return jsonify({"message": "Login successful!"}), 200


#get user info by username
@app.route('/user/get-info', methods=['GET'])
def get_user_info(user_name):
    data = request.get_json()
    print("Received request for user info:", data["user_name"])
    user_name = data["user_name"]
    user = user_helper.get_user_by_username(user_helper.db, user_name)
    
    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        "user_name": user["user_name"],
        "first_name": user["first_name"],
        "last_name": user["last_name"],
        "email": user["email"],
        "monthly_income": user["monthly_income"]
    }), 200




def home():
    return 'Flask is running!'


if __name__ == '__main__':
    app.run(debug=True)