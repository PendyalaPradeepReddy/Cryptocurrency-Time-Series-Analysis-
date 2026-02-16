"""
SARIMA Model for Time Series Forecasting with Seasonality
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
    from statsmodels.tsa.statespace.sarimax import SARIMAX
    SARIMA_AVAILABLE = True
except ImportError:
    SARIMA_AVAILABLE = False
    print("Warning: statsmodels/pmdarima not installed. SARIMA model will not be available.")


class SARIMAModel:
    """SARIMA Model for cryptocurrency price forecasting with seasonality"""
    
    def __init__(self, seasonal_period: int = None):
        self.model = None
        self.fitted_model = None
        self.order = None
        self.seasonal_order = None
        self.seasonal_period = seasonal_period or config.SARIMA_SEASONAL_PERIOD
        self.train_data = None
        self.predictions = None
        self.model_name = "SARIMA"
    
    def auto_select_order(self, series: pd.Series) -> tuple:
        """
        Automatically select best SARIMA orders using AIC
        
        Args:
            series: Time series data
        
        Returns:
            Tuple of ((p,d,q), (P,D,Q,m)) orders
        """
        if not SARIMA_AVAILABLE:
            return ((2, 1, 2), (1, 1, 1, self.seasonal_period))
        
        print(f"Auto-selecting SARIMA order with seasonal period={self.seasonal_period}...")
        
        try:
            auto_model = pm.auto_arima(
                series,
                start_p=1, start_q=1,
                max_p=config.ARIMA_MAX_P,
                max_d=config.ARIMA_MAX_D,
                max_q=config.ARIMA_MAX_Q,
                start_P=0, start_Q=0,
                max_P=2, max_Q=2,
                m=self.seasonal_period,
                seasonal=True,
                trace=False,
                error_action='ignore',
                suppress_warnings=True,
                stepwise=True,
                n_fits=10
            )
            
            self.order = auto_model.order
            self.seasonal_order = auto_model.seasonal_order
            print(f"Selected order: {self.order}, seasonal: {self.seasonal_order}")
            return (self.order, self.seasonal_order)
            
        except Exception as e:
            print(f"Auto-selection failed: {e}. Using default order.")
            self.order = (2, 1, 2)
            self.seasonal_order = (1, 1, 1, self.seasonal_period)
            return (self.order, self.seasonal_order)
    
    def fit(self, series: pd.Series, order: tuple = None, seasonal_order: tuple = None):
        """
        Fit SARIMA model
        
        Args:
            series: Time series data (prices)
            order: (p, d, q) order, if None will auto-select
            seasonal_order: (P, D, Q, m) seasonal order
        """
        if not SARIMA_AVAILABLE:
            raise ImportError("statsmodels and pmdarima are required for SARIMA")
        
        self.train_data = series.copy()
        
        # Auto-select order if not provided
        if order is None or seasonal_order is None:
            self.auto_select_order(series)
        else:
            self.order = order
            self.seasonal_order = seasonal_order
        
        print(f"Fitting SARIMA{self.order}x{self.seasonal_order} model...")
        
        try:
            self.model = SARIMAX(
                series,
                order=self.order,
                seasonal_order=self.seasonal_order,
                enforce_stationarity=False,
                enforce_invertibility=False
            )
            self.fitted_model = self.model.fit(disp=False)
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
            'order': self.order,
            'seasonal_order': self.seasonal_order
        }
    
    def save_model(self, filepath: str = None):
        """Save fitted model to file"""
        if filepath is None:
            filepath = os.path.join(config.MODELS_DIR, 'sarima_model.pkl')
        
        with open(filepath, 'wb') as f:
            pickle.dump({
                'model': self.fitted_model,
                'order': self.order,
                'seasonal_order': self.seasonal_order,
                'train_data': self.train_data
            }, f)
        print(f"Model saved to {filepath}")
    
    def load_model(self, filepath: str = None):
        """Load fitted model from file"""
        if filepath is None:
            filepath = os.path.join(config.MODELS_DIR, 'sarima_model.pkl')
        
        with open(filepath, 'rb') as f:
            data = pickle.load(f)
            self.fitted_model = data['model']
            self.order = data['order']
            self.seasonal_order = data['seasonal_order']
            self.train_data = data['train_data']
        print(f"Model loaded from {filepath}")


def train_sarima(series: pd.Series, horizon: int = 7, seasonal_period: int = 7) -> pd.DataFrame:
    """
    Convenience function to train SARIMA and get forecasts
    
    Args:
        series: Price series
        horizon: Forecast horizon in days
        seasonal_period: Seasonal period (default 7 for weekly)
    
    Returns:
        DataFrame with forecasts
    """
    model = SARIMAModel(seasonal_period=seasonal_period)
    model.fit(series)
    predictions = model.predict(horizon)
    return predictions


if __name__ == "__main__":
    # Test SARIMA model
    print("Testing SARIMA model...")
    
    # Create sample data with weekly seasonality
    np.random.seed(42)
    dates = pd.date_range(start='2023-01-01', periods=100, freq='D')
    trend = np.linspace(50000, 55000, 100)
    seasonality = 500 * np.sin(np.arange(100) * 2 * np.pi / 7)
    noise = np.random.randn(100) * 300
    prices = trend + seasonality + noise
    series = pd.Series(prices, index=dates)
    
    # Train and predict
    model = SARIMAModel(seasonal_period=7)
    model.fit(series)
    forecast = model.predict(horizon=7)
    
    print("\nForecast:")
    print(forecast)
    print("\nMetrics:", model.get_metrics())
