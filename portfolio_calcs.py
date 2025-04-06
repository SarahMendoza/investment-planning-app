import pandas as pd
import yfinance as yf
from pypfopt import expected_returns, risk_models
import numpy as np

def calculate_portfolio_performance(tickers, weights):
    """
    Calculate the return (expected) and risk (volatility) of a portfolio given tickers and weights.
    
    Parameters:
    - tickers (list): List of stock tickers (e.g., ['AAPL', 'GOOGL']).
    - weights (list): List of portfolio weights corresponding to each stock in the tickers list.
    
    Returns:
    - portfolio_return (float): The expected portfolio return.
    - portfolio_risk (float): The total portfolio risk (volatility).
    """
    
    # Download historical adjusted close prices for the given tickers
    data = yf.download(tickers)['Close']  # Yahoo Finance will automatically select the time range
    
    # Calculate daily returns
    returns = data.pct_change().dropna()
    
    # Calculate the expected returns and sample covariance matrix
    mu = expected_returns.mean_historical_return(data)  # Expected returns for each stock
    S = risk_models.sample_cov(data)  # Covariance matrix for the returns
    
    # Ensure weights sum to 1 (you can adjust this if necessary)
    weights = np.array(weights)
    if weights.sum() != 1:
        weights = weights / weights.sum()  # Normalize to make sure weights sum to 1
    
    # Calculate portfolio expected return (weighted average of individual returns)
    portfolio_return = np.dot(weights, mu)
    
    # Calculate portfolio variance
    portfolio_variance = np.dot(weights.T, np.dot(S, weights))
    
    # Calculate portfolio risk (volatility)
    portfolio_risk = np.sqrt(portfolio_variance)
    
    return portfolio_return, portfolio_risk

# # Example usage
# tickers = ['AAPL', 'GOOGL', 'MSFT']  # List of stock tickers
# weights = [0.4, 0.4, 0.2]  # Portfolio weights for AAPL, GOOGL, MSFT

# portfolio_return, portfolio_risk = calculate_portfolio_performance(tickers, weights)
# print(f"Portfolio Expected Return: {portfolio_return:.4f}")
# print(f"Portfolio Risk (Volatility): {portfolio_risk:.4f}")

def calculate_risk_and_return(ticker, start_date, end_date):
    """
    Calculate the risk (volatility) and return rate of the investment based on historical data from Yahoo Finance.

    Args:
        ticker (str): The stock or asset ticker (e.g., 'AAPL', 'GOOG').
        start_date (str): Start date of the historical data (e.g., '2022-01-01').
        end_date (str): End date of the historical data (e.g., '2023-01-01').

    Returns:
        tuple: (risk, return_rate)
    """
    # Fetch historical data for the given ticker
    data = yf.download(ticker, start=start_date, end=end_date)
    
    # Calculate daily percentage change (returns)
    data['Daily Return'] = data['Adj Close'].pct_change()

    # Calculate risk (volatility) as standard deviation of daily returns
    risk = data['Daily Return'].std()

    # Calculate return rate as the total percentage change from start to end date
    return_rate = (data['Adj Close'][-1] - data['Adj Close'][0]) / data['Adj Close'][0]

    return risk, return_rate

def calculate_savings_return(principal, interest_rate, years):
    """
    Calculate the return on a savings account over a period of time.
    """
    return principal * interest_rate * years