# file for storing 


import yfinance as yf
from flask import Flask, jsonify, request
from flask_cors import CORS
import json

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


## APIs for authentication & user operations

    #validate unique username
@app.route('/user/create/unique-user', methods=['POST'])
def unique_username():
    data = request.get_json()
    print("Received user creation request:", data)

    # query the database to check if the username already exists
    
    return jsonify({"message": "User created successfully!"}), 201


@app.route('/user/create', methods=['POST'])
def create_user():
    data = request.get_json()
    print("Received user creation request:", data)

    # save user to MongoDB

    return jsonify({"message": "User created successfully!"}), 201


def home():
    return 'Flask is running!'


if __name__ == '__main__':
    app.run(debug=True)