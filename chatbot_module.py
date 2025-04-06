#from gemini import GeminiAPI
#from google import genai
from pymongo import MongoClient
from datetime import datetime, timedelta
from user_db_module import create_portfolio

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

import re
import requests
from flask import Flask, request, jsonify

# Example API base URL and headers for stock analysis
BASE_URL = 'https://your-stock-analysis-api.com'  # Replace with your actual API base URL
headers = {
    'Authorization': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NDM5NDA0NjUsImlhdCI6MTc0MzkzNjg2NSwic3ViIjoidXNlcl9pZCJ9.1nPu1rWrV2UzatwRYSOXxfW3NONrpJIASc6GOjJXLEk'  # Replace with your actual API key
}

# Function to extract stock ticker from user message
def extract_stock_ticker(user_message):
    # Use regex to find stock tickers (assumes tickers are uppercase letters like 'AAPL')
    ticker_match = re.search(r'\b([A-Z]{1,5})\b', user_message)
    if ticker_match:
        return ticker_match.group(1)
    return None


def get_stock_risk(ticker):
    response = requests.get(
        f'{BASE_URL}/analyze/{ticker}', 
        headers=headers
    )
    
    if response.status_code == 200:
        return response.json()  # Assuming the response is in JSON format
    else:
        return None

import portfolio_calcs as pc

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os

# Connect to MongoDB (make sure MongoDB is running)
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

conversation_collection = db['conversations']

# from google import genai

# client = genai.Client(api_key="AlzaSyDBo4ij2492hJuMyOWtirMZAESLySp1uXM")

# response = client.models.generate_content(
#     model="gemini-2.0-flash", contents="Explain how AI works in a few words"
# )
# print(response.text)

from flask import Flask, request, jsonify
import torch
from google import genai
from google import genai
import torch

# Initialize Gemini Client

import pymongo
from pymongo import MongoClient
import datetime
from google import genai

gemini_client = genai.Client(api_key="AIzaSyBDdMcUQZ6QlHUvKSC6J9bX804mRo9uCuM")

# Function to save message history to MongoDB
def save_message(user_id, user_message, model_response):
    # Store the current conversation
    conversation_data = {
        "user_id": user_id,
        "timestamp": datetime.datetime.now(),  # Timestamp for when the message was saved
        "conversation": [
            {
                "sender": "user",
                "message": user_message
            },
            {
                "sender": "model",
                "message": model_response
            }
        ]
    }

    # Insert or update the conversation history in MongoDB
    conversation_collection.update_one(
        {"user_id": user_id},
        {"$push": {"conversation": {"sender": "user", "message": user_message}}},
        upsert=True
    )
    
    # Insert model response
    conversation_collection.update_one(
        {"user_id": user_id},
        {"$push": {"conversation": {"sender": "model", "message": model_response}}},
        upsert=True
    )

    print(f"Conversation for user {user_id} updated successfully.")

import yfinance as yf

# Fetch stock data for a specific company (e.g., Apple)
def get_stock_data(ticker):
    stock = yf.Ticker(ticker)
    
    # Fetching the stock's history (e.g., last 5 days of data)
    historical_data = stock.history(period="1y")
    
    # Fetching the stock's current info
    current_info = stock.info

    return historical_data, current_info

import yfinance as yf
import numpy as np

def calculate_beta(ticker, market_ticker="SPY", period="1y"):
    stock = yf.Ticker(ticker)
    market = yf.Ticker(market_ticker)
    
    # Get historical data
    stock_data = stock.history(period=period)['Close']
    market_data = market.history(period=period)['Close']
    
    # Calculate daily returns for both stock and market
    stock_returns = stock_data.pct_change().dropna()
    market_returns = market_data.pct_change().dropna()
    
    # Calculate the covariance of the stock with the market and the variance of the market
    covariance = np.cov(stock_returns, market_returns)[0][1]
    market_variance = np.var(market_returns)
    
    # Calculate Beta
    beta = covariance / market_variance
    return beta


# Function to generate investment advice
def generate_investment_advice(user_id, user_input, tone="professional", length="short"):

    user_data = db['users'].find_one({"user_id": user_id})  # Assuming a 'users' collection exists

    if user_data:
        income = user_data["income"]
        age = user_data["age"]
        goals = ", ".join(user_data["goals"])
        budget = user_data["budget"]
        stock_portfolio = user_data["stock_portfolio"]
        time_horizon = user_data["time_horizon"]

        if stock_portfolio["stocks"]:
        # Pull stock data and calculate risk metrics
            for stock_ticker in stock_portfolio["stocks"]:
                
                # Fetch stock data from the API
                stock_data = get_stock_data(stock_ticker)
                current_prices = []
                risk_levels = []
                if stock_data:
                    current_prices.append(stock_data.get('current_price', 'N/A'))
                    risk_levels.append(stock_data.get('risk_level', 'N/A'))

        # Craft a risk analysis message
        risk_message = f"The volatility of {stock_ticker[0]} over the past year is {risk_levels[0]:.2%}. " \
                       f"The beta of {stock_ticker[0]} is {calculate_beta(stock_ticker[0]):.2f}, meaning it is {'more' if calculate_beta(stock_ticker[0]) > 1 else 'less'} volatile than the market."
        
        for i in range(1, len(stock_portfolio["stocks"])):
            risk_message += f"\nThe volatility of {stock_ticker[i]} over the past year is {risk_levels[i]:.2%}. " \
                            f"The beta of {stock_ticker[i]} is {calculate_beta(stock_ticker[i]):.2f}, meaning it is {'more' if calculate_beta(stock_ticker[i]) > 1 else 'less'} volatile than the market."
            i += 1

        
        
        # Build the prompt for investment advice
        prompt = f"User's age: {age}, income: {income}, investment goals: {goals}, time_horizon: {time_horizon}, monthly budget: {budget}, . Based on this, " \
                 f"here's a risk analysis for stocks: {risk_message}." \
                 f"when asked about a specific stock, like 'MSFT', please provide the current risk level: {get_stock_risk(extract_stock_ticker(user_input))}. " \

    # Generate advice using Gemini model
    generated_advice = generate_content_with_gemini(user_input, tone, length)

    # Save the user's input and the AI-generated response to MongoDB
    save_message(user_id, user_input, generated_advice)
    
    return generated_advice

# Function to call the Gemini model and generate content
def generate_content_with_gemini(contents, tone="professional", length="short"):
    # Modify the prompt to reflect the tone and length
    prompt = f"Please provide investment advice in a {tone} and {length} manner. \n\n{contents}"
    
    response = gemini_client.models.generate_content(
        model="gemini-2.0-flash", contents=prompt
    )
    
    return response.text

# Function to get conversation history from MongoDB
def get_conversation_history(user_id):
    # Retrieve the conversation history from MongoDB
    conversation = conversation_collection.find_one({"user_id": user_id})
    
    if conversation:
        # Return the conversation history
        return conversation['conversation']
    else:
        return "No conversation history found."

# Example usage
if __name__ == '__main__':
    # Simulate user input
    create_portfolio(db, "sarahj123", 12, 5000, investment_split = [0.5, 0.5], stocks=['APPL', 'XOM'])
    user_id = "sarahj123"  # Example user ID
    user_message = "What should I invest in today?"

    # Generate investment advice
    investment_advice = generate_investment_advice(user_id, user_message, tone="professional", length="short")

    # Print the advice
    print(f"Investment Advice: {investment_advice}")

    user_message = "How about 'MSFT'?"

    # Generate investment advice
    investment_advice = generate_investment_advice(user_id, user_message, tone="professional", length="short")

    # Print the advice
    print(f"Investment Advice: {investment_advice}")

    # Retrieve conversation history
    #history = get_conversation_history(user_id)
    #print("Conversation History:", history)



# # Example function for generating content with Gemini API
# def generate_content_with_gemini(contents):
#     response = client.models.generate_content(
#         model="gemini-2.0-flash", contents=contents
#     )
#     return response.text

# # Main function for getting investment advice
# def generate_investment_advice(user_input):
#     # Step 1: Generate content with Gemini Model (handle user input)
#     generated_content = generate_content_with_gemini(user_input)
    
#     # Step 2: Post-process the generated content to form investment advice
#     investment_advice = postprocess_output(generated_content)
    
#     return investment_advice

# def postprocess_output(generated_content):
#     # Process the content to give meaningful investment advice
#     # Example: Just return the content for now, you could improve this with more logic
#     return f"Investment advice based on the input: {generated_content}"

# # Tokenization example (if using PyTorch or other model-related operations)
# def preprocess_input(user_input):
#     # Convert text input into tensor or model-friendly format
#     tokens = tokenize(user_input)  # Tokenization example
#     tensor = torch.tensor(tokens)  # Convert tokens to tensor
#     return tensor

# def tokenize(text):
#     # This function would handle tokenization of the text
#     # A placeholder for actual tokenization logic
#     return [ord(c) for c in text]  # A simple example (not how tokenization usually works)

# # Example: Direct user input and generate investment advice
# if __name__ == '__main__':
#     # Get user input directly in the console
#     user_input = input("Enter your question or input for investment advice: ")

#     # Generate investment advice using the model
#     investment_advice = generate_investment_advice(user_input)
    
#     # Output the investment advice
#     print(f"Generated Investment Advice: {investment_advice}")
