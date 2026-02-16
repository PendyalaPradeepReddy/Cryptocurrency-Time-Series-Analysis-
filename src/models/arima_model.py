"""
ARIMA Model for Time Series Forecasting
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
    import pmdarima as pm
    from statsmodels.tsa.arima.model import ARIMA
    ARIMA_AVAILABLE = True
except ImportError:
    ARIMA_AVAILABLE = False
    print("Warning: pmdarima not installed. ARIMA model will not be available.")


class ARIMAModel:
    """ARIMA Model for cryptocurrency price forecasting"""
    
    def __init__(self):
        self.model = None
        self.fitted_model = None
        self.order = None
        self.train_data = None
        self.predictions = None
        self.model_name = "ARIMA"
    
    def auto_select_order(self, series: pd.Series) -> tuple:
        """
        Automatically select best ARIMA order using AIC
        
        Args:
            series: Time series data
        
        Returns:
            Tuple of (p, d, q) order
        """
        if not ARIMA_AVAILABLE:
            return (2, 1, 2)  # Default order
        
        print("Auto-selecting ARIMA order...")
        
        try:
            auto_model = pm.auto_arima(
                series,
                start_p=1, start_q=1,
                max_p=config.ARIMA_MAX_P,
                max_d=config.ARIMA_MAX_D,
                max_q=config.ARIMA_MAX_Q,
                seasonal=False,
                trace=False,
                error_action='ignore',
                suppress_warnings=True,
                stepwise=True
            )
            
            self.order = auto_model.order
            print(f"Selected order: {self.order}")
            return self.order
            
        except Exception as e:
            print(f"Auto-selection failed: {e}. Using default order.")
            self.order = (2, 1, 2)
            return self.order
    
    def fit(self, series: pd.Series, order: tuple = None):
        """
        Fit ARIMA model
        
        Args:
            series: Time series data (prices)
            order: (p, d, q) order, if None will auto-select
        """
        if not ARIMA_AVAILABLE:
            raise ImportError("statsmodels and pmdarima are required for ARIMA")
        
        self.train_data = series.copy()
        
        # Auto-select order if not provided
        if order is None:
            self.auto_select_order(series)
        else:
            self.order = order
        
        print(f"Fitting ARIMA{self.order} model...")
        
        try:
            self.model = ARIMA(series, order=self.order)
            self.fitted_model = self.model.fit()
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
        if self.fitted_model is None:
            raise ValueError("Model must be fitted before prediction")
        
        print(f"Generating {horizon}-day forecast...")
        
        # Get forecast
        forecast_result = self.fitted_model.get_forecast(steps=horizon)
        forecast_mean = forecast_result.predicted_mean
        conf_int = forecast_result.conf_int(alpha=0.05)
        
        # Create date index for forecast
        last_date = self.train_data.index[-1] if isinstance(self.train_data.index[-1], datetime) \
                    else datetime.now()
        forecast_dates = pd.date_range(start=last_date + timedelta(days=1), periods=horizon, freq='D')
        
        # Create forecast DataFrame
        predictions = pd.DataFrame({
            'date': forecast_dates,
            'forecast': forecast_mean.values,
            'lower_ci': conf_int.iloc[:, 0].values,
            'upper_ci': conf_int.iloc[:, 1].values
        })
        
        self.predictions = predictions
        return predictions
    
    def get_model_summary(self) -> str:
        """Get model summary"""
        if self.fitted_model is None:
            return "Model not fitted"
        return str(self.fitted_model.summary())
    
    def get_metrics(self) -> dict:
        """Get model metrics"""
        if self.fitted_model is None:
            return {}
        
        return {
            'aic': self.fitted_model.aic,
            'bic': self.fitted_model.bic,
            'order': self.order
        }
    
    def save_model(self, filepath: str = None):
        """Save fitted model to file"""
        if filepath is None:
            filepath = os.path.join(config.MODELS_DIR, 'arima_model.pkl')
        
        with open(filepath, 'wb') as f:
            pickle.dump({
                'model': self.fitted_model,
                'order': self.order,
                'train_data': self.train_data
            }, f)
        print(f"Model saved to {filepath}")
    
    def load_model(self, filepath: str = None):
        """Load fitted model from file"""
        if filepath is None:
            filepath = os.path.join(config.MODELS_DIR, 'arima_model.pkl')
        
        with open(filepath, 'rb') as f:
            data = pickle.load(f)
            self.fitted_model = data['model']
            self.order = data['order']
            self.train_data = data['train_data']
        print(f"Model loaded from {filepath}")


def train_arima(series: pd.Series, horizon: int = 7, order: tuple = None) -> pd.DataFrame:
    """
    Convenience function to train ARIMA and get forecasts
    
    Args:
        series: Price series
        horizon: Forecast horizon in days
        order: ARIMA order (optional)
    
    Returns:
        DataFrame with forecasts
    """
    model = ARIMAModel()
    model.fit(series, order)
    predictions = model.predict(horizon)
    return predictions


if __name__ == "__main__":
    # Test ARIMA model
    print("Testing ARIMA model...")
    
    # Create sample data
    np.random.seed(42)
    dates = pd.date_range(start='2023-01-01', periods=100, freq='D')
    prices = 50000 + np.cumsum(np.random.randn(100) * 500)
    series = pd.Series(prices, index=dates)
    
    # Train and predict
    model = ARIMAModel()
    model.fit(series)
    forecast = model.predict(horizon=7)
    
    print("\nForecast:")
    print(forecast)
    print("\nMetrics:", model.get_metrics())
