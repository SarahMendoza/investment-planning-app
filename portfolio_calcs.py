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
