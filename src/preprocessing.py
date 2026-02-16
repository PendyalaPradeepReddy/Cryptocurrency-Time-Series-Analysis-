"""
Data Preprocessing Module - Cleans data and creates derived features
"""
import os
import sys
import pandas as pd
import numpy as np

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config
from src.utils import (
    calculate_returns, 
    calculate_rolling_mean, 
    calculate_rolling_std,
    calculate_volatility,
    calculate_max_drawdown,
    calculate_sharpe_ratio
)


def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Handle missing values in the dataset
    
    Args:
        df: Raw DataFrame
    
    Returns:
        DataFrame with missing values handled
    """
    df = df.copy()
    
    # Forward fill for price data
    price_cols = ['open', 'high', 'low', 'close']
    for col in price_cols:
        if col in df.columns:
            df[col] = df[col].ffill()
    
    # Fill volume with 0 if missing
    if 'volume' in df.columns:
        df['volume'] = df['volume'].fillna(0)
    
    if 'market_cap' in df.columns:
        df['market_cap'] = df['market_cap'].fillna(0)
    
    return df


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove duplicate entries based on date
    
    Args:
        df: DataFrame with potential duplicates
    
    Returns:
        DataFrame with duplicates removed
    """
    df = df.copy()
    df = df.drop_duplicates(subset=['date'], keep='last')
    df = df.sort_values('date').reset_index(drop=True)
    return df


def ensure_daily_frequency(df: pd.DataFrame) -> pd.DataFrame:
    """
    Ensure data has daily frequency by filling missing dates
    
    Args:
        df: DataFrame with potential gaps
    
    Returns:
        DataFrame with continuous daily data
    """
    df = df.copy()
    df['date'] = pd.to_datetime(df['date'])
    
    # Create complete date range
    date_range = pd.date_range(start=df['date'].min(), end=df['date'].max(), freq='D')
    
    # Reindex to fill missing dates
    df = df.set_index('date')
    df = df.reindex(date_range)
    df = df.ffill()  # Forward fill missing values
    df = df.reset_index()
    df = df.rename(columns={'index': 'date'})
    
    return df


def add_derived_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add derived features for analysis
    
    Args:
        df: Preprocessed DataFrame
    
    Returns:
        DataFrame with additional features
    """
    df = df.copy()
    
    # Daily returns
    df['returns'] = calculate_returns(df['close'])
    df['log_returns'] = np.log(df['close'] / df['close'].shift(1))
    
    # Rolling averages
    df['sma_7'] = calculate_rolling_mean(df['close'], config.ROLLING_WINDOWS['short'])
    df['sma_30'] = calculate_rolling_mean(df['close'], config.ROLLING_WINDOWS['medium'])
    df['sma_90'] = calculate_rolling_mean(df['close'], 90)
    
    # Exponential moving averages
    df['ema_7'] = df['close'].ewm(span=7, adjust=False).mean()
    df['ema_30'] = df['close'].ewm(span=30, adjust=False).mean()
    
    # Volatility (rolling standard deviation of returns)
    df['volatility_7'] = calculate_rolling_std(df['returns'], 7)
    df['volatility_21'] = calculate_rolling_std(df['returns'], 21)
    df['volatility_30'] = calculate_rolling_std(df['returns'], 30)
    
    # Annualized volatility
    df['volatility_annualized'] = df['volatility_21'] * np.sqrt(365)
    
    # Price momentum
    df['momentum_7'] = df['close'] / df['close'].shift(7) - 1
    df['momentum_30'] = df['close'] / df['close'].shift(30) - 1
    
    # Bollinger Bands
    df['bb_middle'] = df['sma_30']
    df['bb_std'] = calculate_rolling_std(df['close'], 30)
    df['bb_upper'] = df['bb_middle'] + 2 * df['bb_std']
    df['bb_lower'] = df['bb_middle'] - 2 * df['bb_std']
    df['bb_width'] = (df['bb_upper'] - df['bb_lower']) / df['bb_middle']
    
    # RSI (Relative Strength Index)
    df['rsi'] = calculate_rsi(df['close'], 14)
    
    # MACD
    df['macd'], df['macd_signal'], df['macd_histogram'] = calculate_macd(df['close'])
    
    # Volume features (if available)
    if 'volume' in df.columns and df['volume'].sum() > 0:
        df['volume_sma_7'] = calculate_rolling_mean(df['volume'], 7)
        df['volume_ratio'] = df['volume'] / df['volume_sma_7']
    
    # Price range
    df['daily_range'] = (df['high'] - df['low']) / df['close']
    
    # Fill any remaining NaN values
    df = df.fillna(method='bfill').fillna(0)
    
    return df


def calculate_rsi(prices: pd.Series, period: int = 14) -> pd.Series:
    """
    Calculate Relative Strength Index
    
    Args:
        prices: Price series
        period: RSI period
    
    Returns:
        RSI series
    """
    delta = prices.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    
    return rsi


def calculate_macd(prices: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9) -> tuple:
    """
    Calculate MACD indicator
    
    Args:
        prices: Price series
        fast: Fast EMA period
        slow: Slow EMA period
        signal: Signal line period
    
    Returns:
        Tuple of (MACD line, Signal line, Histogram)
    """
    ema_fast = prices.ewm(span=fast, adjust=False).mean()
    ema_slow = prices.ewm(span=slow, adjust=False).mean()
    
    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    histogram = macd_line - signal_line
    
    return macd_line, signal_line, histogram


def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Complete preprocessing pipeline
    
    Args:
        df: Raw DataFrame from data collection
    
    Returns:
        Fully preprocessed DataFrame with derived features
    """
    print("Starting preprocessing pipeline...")
    
    # Step 1: Handle missing values
    df = handle_missing_values(df)
    print("  - Handled missing values")
    
    # Step 2: Remove duplicates
    df = remove_duplicates(df)
    print("  - Removed duplicates")
    
    # Step 3: Ensure daily frequency
    df = ensure_daily_frequency(df)
    print("  - Ensured daily frequency")
    
    # Step 4: Add derived features
    df = add_derived_features(df)
    print("  - Added derived features")
    
    print(f"Preprocessing complete. Shape: {df.shape}")
    
    return df


def preprocess_all_coins() -> dict:
    """
    Preprocess data for all configured cryptocurrencies
    
    Returns:
        Dictionary mapping coin_id to preprocessed DataFrame
    """
    processed_data = {}
    
    for coin_id in config.CRYPTO_LIST.keys():
        try:
            # Load raw data
            raw_path = os.path.join(config.RAW_DATA_DIR, f"{coin_id}.csv")
            
            if not os.path.exists(raw_path):
                print(f"No raw data found for {coin_id}, skipping...")
                continue
            
            df = pd.read_csv(raw_path, parse_dates=['date'])
            
            # Preprocess
            df = preprocess_data(df)
            processed_data[coin_id] = df
            
            # Save processed data
            processed_path = os.path.join(config.PROCESSED_DATA_DIR, f"{coin_id}.csv")
            df.to_csv(processed_path, index=False)
            print(f"Saved processed data: {processed_path}")
            
        except Exception as e:
            print(f"Error preprocessing {coin_id}: {e}")
            continue
    
    return processed_data


def load_processed_data(coin_id: str) -> pd.DataFrame:
    """
    Load preprocessed data from CSV
    
    Args:
        coin_id: Cryptocurrency ID
    
    Returns:
        Preprocessed DataFrame
    """
    filepath = os.path.join(config.PROCESSED_DATA_DIR, f"{coin_id}.csv")
    
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"No processed data found for {coin_id}")
    
    df = pd.read_csv(filepath, parse_dates=['date'])
    return df


def get_summary_statistics(df: pd.DataFrame) -> dict:
    """
    Calculate summary statistics for a coin's data
    
    Args:
        df: Preprocessed DataFrame
    
    Returns:
        Dictionary with summary statistics
    """
    stats = {
        'start_date': df['date'].min(),
        'end_date': df['date'].max(),
        'num_days': len(df),
        'current_price': df['close'].iloc[-1],
        'min_price': df['close'].min(),
        'max_price': df['close'].max(),
        'avg_price': df['close'].mean(),
        'total_return': (df['close'].iloc[-1] / df['close'].iloc[0] - 1),
        'volatility_30d': df['volatility_30'].iloc[-1] if 'volatility_30' in df.columns else None,
        'avg_daily_return': df['returns'].mean() if 'returns' in df.columns else None,
        'sharpe_ratio': calculate_sharpe_ratio(df['returns']) if 'returns' in df.columns else None,
        'max_drawdown': calculate_max_drawdown(df['close'])
    }
    
    return stats


if __name__ == "__main__":
    # Test preprocessing
    print("Testing preprocessing pipeline...")
    
    # Load and preprocess sample data
    try:
        btc_raw = pd.read_csv(os.path.join(config.RAW_DATA_DIR, "bitcoin.csv"), parse_dates=['date'])
        btc_processed = preprocess_data(btc_raw)
        print(f"\nProcessed columns: {btc_processed.columns.tolist()}")
        print(f"\nSample data:\n{btc_processed.head()}")
        
        # Get summary statistics
        stats = get_summary_statistics(btc_processed)
        print(f"\nSummary Statistics:")
        for key, value in stats.items():
            print(f"  {key}: {value}")
            
    except FileNotFoundError:
        print("No raw data found. Run data_collection.py first.")
