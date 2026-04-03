"""
Data Loading Module - Loads and processes data from main_df_enhanced.csv
"""
import os
import sys
import pandas as pd
import numpy as np

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config


def load_main_data() -> pd.DataFrame:
    """
    Load the main enhanced dataset
    
    Returns:
        DataFrame with all cryptocurrency data
    """
    # Check if file exists
    if not os.path.exists(config.DATA_FILE):
        raise FileNotFoundError(
            f"Data file not found: {config.DATA_FILE}\n"
            f"Project root: {config.BASE_DIR}\n"
            f"Current directory: {os.getcwd()}"
        )
    
    df = pd.read_csv(config.DATA_FILE)
    
    # Standardize column names
    df.columns = [col.lower() for col in df.columns]
    
    # Parse datetime
    df['date'] = pd.to_datetime(df['datetime'])
    
    # Sort by date and symbol
    df = df.sort_values(['symbol', 'date']).reset_index(drop=True)
    
    return df


def load_coin_data(symbol: str) -> pd.DataFrame:
    """
    Load data for a specific cryptocurrency
    
    Args:
        symbol: Cryptocurrency symbol (e.g., 'BTC', 'ETH')
    
    Returns:
        DataFrame with price data for the coin
    """
    df = load_main_data()
    
    # Filter for the symbol
    coin_df = df[df['symbol'] == symbol].copy()
    
    if coin_df.empty:
        raise ValueError(f"No data found for symbol: {symbol}")
    
    # Rename columns to match expected format
    coin_df = coin_df.rename(columns={
        'open': 'open',
        'high': 'high', 
        'low': 'low',
        'close': 'close',
        'volume': 'volume',
        'sentiment': 'sentiment'
    })
    
    # Add derived features
    coin_df = add_features(coin_df)
    
    return coin_df.reset_index(drop=True)


def add_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add derived features to the dataframe
    
    Args:
        df: Raw price DataFrame
    
    Returns:
        DataFrame with additional features
    """
    df = df.copy()
    
    # Daily returns
    df['returns'] = df['close'].pct_change()
    df['log_returns'] = np.log(df['close'] / df['close'].shift(1))
    
    # Rolling averages
    df['sma_7'] = df['close'].rolling(window=7, min_periods=1).mean()
    df['sma_30'] = df['close'].rolling(window=30, min_periods=1).mean()
    df['sma_90'] = df['close'].rolling(window=90, min_periods=1).mean()
    
    # Exponential moving averages
    df['ema_7'] = df['close'].ewm(span=7, adjust=False).mean()
    df['ema_30'] = df['close'].ewm(span=30, adjust=False).mean()
    
    # Volatility
    df['volatility_7'] = df['returns'].rolling(window=7, min_periods=1).std()
    df['volatility_21'] = df['returns'].rolling(window=21, min_periods=1).std()
    df['volatility_30'] = df['returns'].rolling(window=30, min_periods=1).std()
    
    # Bollinger Bands
    df['bb_middle'] = df['sma_30']
    df['bb_std'] = df['close'].rolling(window=30, min_periods=1).std()
    df['bb_upper'] = df['bb_middle'] + 2 * df['bb_std']
    df['bb_lower'] = df['bb_middle'] - 2 * df['bb_std']
    
    # RSI
    df['rsi'] = calculate_rsi(df['close'], 14)
    
    # MACD
    df['macd'], df['macd_signal'], df['macd_histogram'] = calculate_macd(df['close'])
    
    # Fill NaN values
    df = df.bfill().fillna(0)
    
    return df


def calculate_rsi(prices: pd.Series, period: int = 14) -> pd.Series:
    """Calculate Relative Strength Index"""
    delta = prices.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    
    return rsi


def calculate_macd(prices: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9) -> tuple:
    """Calculate MACD indicator"""
    ema_fast = prices.ewm(span=fast, adjust=False).mean()
    ema_slow = prices.ewm(span=slow, adjust=False).mean()
    
    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    histogram = macd_line - signal_line
    
    return macd_line, signal_line, histogram


def get_available_symbols() -> list:
    """Get list of available cryptocurrency symbols"""
    df = load_main_data()
    return sorted(df['symbol'].unique().tolist())


def get_data_date_range(symbol: str = None) -> tuple:
    """Get the date range of available data"""
    df = load_main_data()
    
    if symbol:
        df = df[df['symbol'] == symbol]
    
    return df['date'].min(), df['date'].max()


if __name__ == "__main__":
    # Test data loading
    print("Testing data loading...")
    
    # Load all data
    df = load_main_data()
    print(f"Total rows: {len(df)}")
    print(f"Symbols: {get_available_symbols()}")
    
    # Load BTC data
    btc_df = load_coin_data('BTC')
    print(f"\nBTC rows: {len(btc_df)}")
    print(f"BTC columns: {btc_df.columns.tolist()}")
    print(f"\nBTC sample:\n{btc_df.head()}")
