"""
Data Collection Module - Fetches cryptocurrency data from CoinGecko API
"""
import os
import sys
import time
import requests
import pandas as pd
from datetime import datetime, timedelta

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config


def fetch_crypto_data(coin_id: str, days: int = None, vs_currency: str = None) -> pd.DataFrame:
    """
    Fetch historical price data for a cryptocurrency from CoinGecko API
    
    Args:
        coin_id: CoinGecko coin ID (e.g., 'bitcoin', 'ethereum', 'solana')
        days: Number of days of historical data (default from config)
        vs_currency: Currency to get prices in (default: 'usd')
    
    Returns:
        DataFrame with columns: date, open, high, low, close, volume
    """
    if days is None:
        days = config.DEFAULT_DAYS
    if vs_currency is None:
        vs_currency = config.VS_CURRENCY
    
    # CoinGecko market chart endpoint
    url = f"{config.COINGECKO_API_URL}/coins/{coin_id}/market_chart"
    params = {
        "vs_currency": vs_currency,
        "days": days,
        "interval": "daily"
    }
    
    print(f"Fetching {days} days of {coin_id} data...")
    
    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        # Extract prices and volumes
        prices = data.get('prices', [])
        volumes = data.get('total_volumes', [])
        market_caps = data.get('market_caps', [])
        
        if not prices:
            raise ValueError(f"No price data received for {coin_id}")
        
        # Create DataFrame
        df = pd.DataFrame(prices, columns=['timestamp', 'close'])
        df['date'] = pd.to_datetime(df['timestamp'], unit='ms').dt.date
        df['date'] = pd.to_datetime(df['date'])
        
        # Add volume data
        if volumes:
            vol_df = pd.DataFrame(volumes, columns=['timestamp', 'volume'])
            df['volume'] = vol_df['volume']
        else:
            df['volume'] = 0
        
        # Add market cap
        if market_caps:
            cap_df = pd.DataFrame(market_caps, columns=['timestamp', 'market_cap'])
            df['market_cap'] = cap_df['market_cap']
        else:
            df['market_cap'] = 0
        
        # For daily data, we'll use close as proxy for OHLC
        # CoinGecko's daily endpoint doesn't provide OHLC
        df['open'] = df['close'].shift(1)
        df['high'] = df['close'] * 1.02  # Approximate
        df['low'] = df['close'] * 0.98   # Approximate
        
        # Clean up first row
        df.loc[0, 'open'] = df.loc[0, 'close']
        
        # Select and order columns
        df = df[['date', 'open', 'high', 'low', 'close', 'volume', 'market_cap']]
        
        # Remove duplicates and sort
        df = df.drop_duplicates(subset=['date'], keep='last')
        df = df.sort_values('date').reset_index(drop=True)
        
        print(f"Successfully fetched {len(df)} days of data for {coin_id}")
        return df
        
    except requests.exceptions.RequestException as e:
        print(f"API Error: {e}")
        raise
    except Exception as e:
        print(f"Error processing data: {e}")
        raise


def fetch_ohlc_data(coin_id: str, days: int = 365, vs_currency: str = "usd") -> pd.DataFrame:
    """
    Fetch OHLC (candlestick) data from CoinGecko
    Note: Free tier only supports 1, 7, 14, 30, 90, 180, 365 days, or 'max'
    
    Args:
        coin_id: CoinGecko coin ID
        days: Number of days (must be 1, 7, 14, 30, 90, 180, 365, or 'max')
        vs_currency: Currency for prices
    
    Returns:
        DataFrame with OHLC data
    """
    url = f"{config.COINGECKO_API_URL}/coins/{coin_id}/ohlc"
    params = {
        "vs_currency": vs_currency,
        "days": days
    }
    
    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        if not data:
            raise ValueError(f"No OHLC data received for {coin_id}")
        
        df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close'])
        df['date'] = pd.to_datetime(df['timestamp'], unit='ms')
        df = df[['date', 'open', 'high', 'low', 'close']]
        
        return df
        
    except Exception as e:
        print(f"Error fetching OHLC data: {e}")
        raise


def fetch_all_coins(days: int = None) -> dict:
    """
    Fetch data for all configured cryptocurrencies
    
    Args:
        days: Number of days of data per coin
    
    Returns:
        Dictionary mapping coin_id to DataFrame
    """
    if days is None:
        days = config.DEFAULT_DAYS
    
    all_data = {}
    
    for coin_id in config.CRYPTO_LIST.keys():
        try:
            df = fetch_crypto_data(coin_id, days)
            all_data[coin_id] = df
            
            # Save raw data
            filepath = os.path.join(config.RAW_DATA_DIR, f"{coin_id}.csv")
            df.to_csv(filepath, index=False)
            print(f"Saved raw data: {filepath}")
            
            # Rate limiting
            time.sleep(config.API_RATE_LIMIT_DELAY)
            
        except Exception as e:
            print(f"Failed to fetch {coin_id}: {e}")
            continue
    
    return all_data


def load_raw_data(coin_id: str) -> pd.DataFrame:
    """
    Load raw data from CSV file
    
    Args:
        coin_id: Cryptocurrency ID
    
    Returns:
        DataFrame with raw price data
    """
    filepath = os.path.join(config.RAW_DATA_DIR, f"{coin_id}.csv")
    
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"No data file found for {coin_id}. Run fetch_crypto_data first.")
    
    df = pd.read_csv(filepath, parse_dates=['date'])
    return df


def get_coin_info(coin_id: str) -> dict:
    """
    Get detailed information about a cryptocurrency
    
    Args:
        coin_id: CoinGecko coin ID
    
    Returns:
        Dictionary with coin information
    """
    url = f"{config.COINGECKO_API_URL}/coins/{coin_id}"
    params = {
        "localization": "false",
        "tickers": "false",
        "community_data": "false",
        "developer_data": "false"
    }
    
    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching coin info: {e}")
        return {}


if __name__ == "__main__":
    # Test data collection
    print("Testing data collection...")
    
    # Fetch Bitcoin data
    btc_data = fetch_crypto_data("bitcoin", days=30)
    print(f"\nBitcoin data shape: {btc_data.shape}")
    print(btc_data.head())
    print(btc_data.tail())
