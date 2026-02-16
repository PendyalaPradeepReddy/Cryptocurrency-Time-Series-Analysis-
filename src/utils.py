"""
Utility functions for cryptocurrency analysis
"""
import os
import sys
import pandas as pd
import numpy as np
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def ensure_directories():
    """Create necessary directories if they don't exist"""
    import config
    for dir_path in [config.RAW_DATA_DIR, config.PROCESSED_DATA_DIR, config.MODELS_DIR]:
        os.makedirs(dir_path, exist_ok=True)


def calculate_returns(prices: pd.Series) -> pd.Series:
    """Calculate daily returns from price series"""
    return prices.pct_change()


def calculate_rolling_mean(series: pd.Series, window: int) -> pd.Series:
    """Calculate rolling mean"""
    return series.rolling(window=window, min_periods=1).mean()


def calculate_rolling_std(series: pd.Series, window: int) -> pd.Series:
    """Calculate rolling standard deviation (volatility)"""
    return series.rolling(window=window, min_periods=1).std()


def calculate_volatility(returns: pd.Series, window: int = 21) -> pd.Series:
    """Calculate annualized volatility from returns"""
    rolling_std = returns.rolling(window=window, min_periods=1).std()
    return rolling_std * np.sqrt(365)  # Annualized for crypto (365 days)


def calculate_sharpe_ratio(returns: pd.Series, risk_free_rate: float = 0.02) -> float:
    """Calculate Sharpe ratio"""
    excess_returns = returns.mean() * 365 - risk_free_rate
    volatility = returns.std() * np.sqrt(365)
    return excess_returns / volatility if volatility != 0 else 0


def calculate_max_drawdown(prices: pd.Series) -> float:
    """Calculate maximum drawdown"""
    peak = prices.expanding(min_periods=1).max()
    drawdown = (prices - peak) / peak
    return drawdown.min()


def calculate_var(returns: pd.Series, confidence: float = 0.95) -> float:
    """Calculate Value at Risk at given confidence level"""
    return np.percentile(returns.dropna(), (1 - confidence) * 100)


def format_currency(value: float) -> str:
    """Format value as currency string"""
    if abs(value) >= 1e9:
        return f"${value/1e9:.2f}B"
    elif abs(value) >= 1e6:
        return f"${value/1e6:.2f}M"
    elif abs(value) >= 1e3:
        return f"${value/1e3:.2f}K"
    else:
        return f"${value:.2f}"


def format_percentage(value: float) -> str:
    """Format value as percentage string"""
    return f"{value * 100:.2f}%"


def get_date_range_str(df: pd.DataFrame, date_col: str = 'date') -> str:
    """Get date range string from dataframe"""
    start = df[date_col].min()
    end = df[date_col].max()
    return f"{start.strftime('%Y-%m-%d')} to {end.strftime('%Y-%m-%d')}"


def resample_to_daily(df: pd.DataFrame, date_col: str = 'date') -> pd.DataFrame:
    """Resample data to daily frequency"""
    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col])
    df = df.set_index(date_col)
    df = df.resample('D').ffill()
    return df.reset_index()


def train_test_split_ts(df: pd.DataFrame, test_size: float = 0.2) -> tuple:
    """Time series aware train-test split"""
    split_idx = int(len(df) * (1 - test_size))
    train = df.iloc[:split_idx].copy()
    test = df.iloc[split_idx:].copy()
    return train, test


def create_sequences(data: np.ndarray, lookback: int) -> tuple:
    """Create sequences for LSTM training"""
    X, y = [], []
    for i in range(lookback, len(data)):
        X.append(data[i-lookback:i])
        y.append(data[i])
    return np.array(X), np.array(y)


def save_dataframe(df: pd.DataFrame, filepath: str):
    """Save DataFrame to CSV"""
    df.to_csv(filepath, index=False)
    print(f"Saved: {filepath}")


def load_dataframe(filepath: str) -> pd.DataFrame:
    """Load DataFrame from CSV"""
    df = pd.read_csv(filepath, parse_dates=['date'])
    return df
