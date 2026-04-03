"""
Configuration settings for Cryptocurrency Time Series Analysis
"""
import os
from datetime import datetime, timedelta

# Project Paths - Use absolute path resolution to work with Streamlit deployment
def get_project_root():
    """Get the project root directory reliably"""
    # Get the directory where this config.py file is located
    config_dir = os.path.dirname(os.path.abspath(__file__))
    return config_dir

BASE_DIR = get_project_root()
DATA_DIR = os.path.join(BASE_DIR, "data")
RAW_DATA_DIR = os.path.join(DATA_DIR, "raw")
PROCESSED_DATA_DIR = os.path.join(DATA_DIR, "processed")
MODELS_DIR = os.path.join(BASE_DIR, "models", "saved")

# Create directories if they don't exist
for dir_path in [RAW_DATA_DIR, PROCESSED_DATA_DIR, MODELS_DIR]:
    os.makedirs(dir_path, exist_ok=True)

# API Configuration
COINGECKO_API_URL = "https://api.coingecko.com/api/v3"
API_RATE_LIMIT_DELAY = 1.5  # seconds between API calls

# Supported Cryptocurrencies (from main_df_enhanced.csv)
CRYPTO_LIST = {
    "BTC": {"symbol": "BTC", "name": "Bitcoin"},
    "ETH": {"symbol": "ETH", "name": "Ethereum"},
    "ADA": {"symbol": "ADA", "name": "Cardano"},
    "DOGE": {"symbol": "DOGE", "name": "Dogecoin"},
    "XRP": {"symbol": "XRP", "name": "Ripple"},
    "DOT": {"symbol": "DOT", "name": "Polkadot"},
    "LINK": {"symbol": "LINK", "name": "Chainlink"},
    "LTC": {"symbol": "LTC", "name": "Litecoin"},
    "UNI": {"symbol": "UNI", "name": "Uniswap"},
    "BCH": {"symbol": "BCH", "name": "Bitcoin Cash"},
    "ALGO": {"symbol": "ALGO", "name": "Algorand"},
    "AAVE": {"symbol": "AAVE", "name": "Aave"},
    "EOS": {"symbol": "EOS", "name": "EOS"},
    "ETC": {"symbol": "ETC", "name": "Ethereum Classic"},
    "FIL": {"symbol": "FIL", "name": "Filecoin"},
    "GRT": {"symbol": "GRT", "name": "The Graph"},
    "XLM": {"symbol": "XLM", "name": "Stellar"}
}

# Data file path - with fallback for Streamlit Cloud
DATA_FILE = os.path.join(BASE_DIR, "main_df_enhanced.csv")
if not os.path.exists(DATA_FILE):
    # Fallback: try to find it in parent directory (in case running from subdirectory)
    parent_data_file = os.path.join(os.path.dirname(BASE_DIR), "main_df_enhanced.csv")
    if os.path.exists(parent_data_file):
        DATA_FILE = parent_data_file

# Data Collection Settings
DEFAULT_DAYS = 1095  # ~3 years of data
VS_CURRENCY = "usd"

# Preprocessing Settings
ROLLING_WINDOWS = {
    "short": 7,
    "medium": 30,
    "volatility": 21
}

# Model Settings
FORECAST_HORIZONS = {
    "short": 7,
    "long": 30
}

# ARIMA Settings
ARIMA_MAX_P = 5
ARIMA_MAX_D = 2
ARIMA_MAX_Q = 5

# SARIMA Settings
SARIMA_SEASONAL_PERIOD = 7  # Weekly seasonality

# LSTM Settings
LSTM_CONFIG = {
    "lookback": 60,
    "units": 50,
    "epochs": 50,
    "batch_size": 32,
    "validation_split": 0.1
}

# Prophet Settings
PROPHET_CONFIG = {
    "yearly_seasonality": True,
    "weekly_seasonality": True,
    "daily_seasonality": False,
    "changepoint_prior_scale": 0.05
}

# Dashboard Settings
DASHBOARD_TITLE = "Crypto Analytics Dashboard"
DEFAULT_COIN = "bitcoin"
CHART_THEME = "plotly_dark"
