"""
Prophet Model for Time Series Forecasting
"""
import os
import sys
import pandas as pd
import numpy as np
import warnings
import pickle
from datetime import datetime, timedelta

warnings.filterwarnings('ignore')

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import config

try:
    from prophet import Prophet
    PROPHET_AVAILABLE = True
except ImportError:
    PROPHET_AVAILABLE = False
    print("Warning: prophet not installed. Prophet model will not be available.")


class ProphetModel:
    """Facebook Prophet Model for cryptocurrency price forecasting"""
    
    def __init__(self):
        self.model = None
        self.train_data = None
        self.predictions = None
        self.model_name = "Prophet"
        self.config = config.PROPHET_CONFIG
    
    def prepare_data(self, df: pd.DataFrame, date_col: str = 'date', 
                     value_col: str = 'close') -> pd.DataFrame:
        """
        Prepare data for Prophet (requires 'ds' and 'y' columns)
        
        Args:
            df: Input DataFrame
            date_col: Date column name
            value_col: Value column name
        
        Returns:
            Prophet-formatted DataFrame
        """
        prophet_df = pd.DataFrame({
            'ds': pd.to_datetime(df[date_col]),
            'y': df[value_col].values
        })
        return prophet_df
    
    def fit(self, df: pd.DataFrame, date_col: str = 'date', value_col: str = 'close'):
        """
        Fit Prophet model
        
        Args:
            df: DataFrame with date and price columns
            date_col: Name of date column
            value_col: Name of value column
        """
        if not PROPHET_AVAILABLE:
            raise ImportError("prophet is required for this model")
        
        # Prepare data
        self.train_data = self.prepare_data(df, date_col, value_col)
        
        print("Fitting Prophet model...")
        
        try:
            # Initialize model with config
            self.model = Prophet(
                yearly_seasonality=self.config['yearly_seasonality'],
                weekly_seasonality=self.config['weekly_seasonality'],
                daily_seasonality=self.config['daily_seasonality'],
                changepoint_prior_scale=self.config['changepoint_prior_scale']
            )
            
            # Add custom seasonalities for crypto
            self.model.add_seasonality(
                name='monthly',
                period=30.5,
                fourier_order=5
            )
            
            # Fit model
            self.model.fit(self.train_data)
            print("Model fitted successfully")
            
        except Exception as e:
            print(f"Error fitting model: {e}")
            raise
    
    def predict(self, horizon: int = 7) -> pd.DataFrame:
        """
        Generate forecasts
        
        Args:
            horizon: Number of days to forecast
        
        Returns:
            DataFrame with forecasts and confidence intervals
        """
        if self.model is None:
            raise ValueError("Model must be fitted before prediction")
        
        print(f"Generating {horizon}-day forecast...")
        
        # Create future dataframe
        future = self.model.make_future_dataframe(periods=horizon)
        
        # Generate forecast
        forecast = self.model.predict(future)
        
        # Extract predictions for forecast period only
        forecast_period = forecast.tail(horizon)
        
        predictions = pd.DataFrame({
            'date': forecast_period['ds'].values,
            'forecast': forecast_period['yhat'].values,
            'lower_ci': forecast_period['yhat_lower'].values,
            'upper_ci': forecast_period['yhat_upper'].values,
            'trend': forecast_period['trend'].values
        })
        
        self.predictions = predictions
        return predictions
    
    def get_components(self) -> dict:
        """
        Get decomposed components (trend, seasonality, etc.)
        
        Returns:
            Dictionary with component DataFrames
        """
        if self.model is None:
            return {}
        
        future = self.model.make_future_dataframe(periods=0)
        forecast = self.model.predict(future)
        
        components = {
            'trend': forecast[['ds', 'trend']],
            'weekly': forecast[['ds', 'weekly']] if 'weekly' in forecast.columns else None,
            'yearly': forecast[['ds', 'yearly']] if 'yearly' in forecast.columns else None
        }
        
        return components
    
    def plot_components(self):
        """Plot forecast components"""
        if self.model is None:
            print("Model not fitted")
            return None
        
        future = self.model.make_future_dataframe(periods=30)
        forecast = self.model.predict(future)
        
        fig = self.model.plot_components(forecast)
        return fig
    
    def get_changepoints(self) -> pd.DataFrame:
        """Get detected changepoints"""
        if self.model is None:
            return pd.DataFrame()
        
        changepoints = pd.DataFrame({
            'date': self.model.changepoints,
            'rate_change': self.model.params['delta'].mean(axis=0)
        })
        
        return changepoints
    
    def get_metrics(self) -> dict:
        """Get model configuration metrics"""
        return {
            'yearly_seasonality': self.config['yearly_seasonality'],
            'weekly_seasonality': self.config['weekly_seasonality'],
            'changepoint_prior_scale': self.config['changepoint_prior_scale']
        }
    
    def save_model(self, filepath: str = None):
        """Save fitted model to file"""
        if filepath is None:
            filepath = os.path.join(config.MODELS_DIR, 'prophet_model.pkl')
        
        with open(filepath, 'wb') as f:
            pickle.dump({
                'model': self.model,
                'train_data': self.train_data
            }, f)
        print(f"Model saved to {filepath}")
    
    def load_model(self, filepath: str = None):
        """Load fitted model from file"""
        if filepath is None:
            filepath = os.path.join(config.MODELS_DIR, 'prophet_model.pkl')
        
        with open(filepath, 'rb') as f:
            data = pickle.load(f)
            self.model = data['model']
            self.train_data = data['train_data']
        print(f"Model loaded from {filepath}")


def train_prophet(df: pd.DataFrame, horizon: int = 7, 
                  date_col: str = 'date', value_col: str = 'close') -> pd.DataFrame:
    """
    Convenience function to train Prophet and get forecasts
    
    Args:
        df: DataFrame with price data
        horizon: Forecast horizon in days
        date_col: Date column name
        value_col: Value column name
    
    Returns:
        DataFrame with forecasts
    """
    model = ProphetModel()
    model.fit(df, date_col, value_col)
    predictions = model.predict(horizon)
    return predictions


if __name__ == "__main__":
    # Test Prophet model
    print("Testing Prophet model...")
    
    # Create sample data
    np.random.seed(42)
    dates = pd.date_range(start='2023-01-01', periods=365, freq='D')
    trend = np.linspace(50000, 55000, 365)
    seasonality = 1000 * np.sin(np.arange(365) * 2 * np.pi / 365)  # Yearly
    weekly = 500 * np.sin(np.arange(365) * 2 * np.pi / 7)  # Weekly
    noise = np.random.randn(365) * 300
    prices = trend + seasonality + weekly + noise
    
    df = pd.DataFrame({
        'date': dates,
        'close': prices
    })
    
    # Train and predict
    model = ProphetModel()
    model.fit(df)
    forecast = model.predict(horizon=7)
    
    print("\nForecast:")
    print(forecast)
