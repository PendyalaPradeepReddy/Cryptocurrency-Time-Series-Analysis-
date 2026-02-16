"""
LSTM Model for Time Series Forecasting
"""
import os
import sys
import pandas as pd
import numpy as np
import warnings
import pickle
from datetime import datetime, timedelta

warnings.filterwarnings('ignore')
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Suppress TF warnings

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import config

try:
    import tensorflow as tf
    from tensorflow.keras.models import Sequential, load_model
    from tensorflow.keras.layers import LSTM, Dense, Dropout
    from tensorflow.keras.callbacks import EarlyStopping
    from sklearn.preprocessing import MinMaxScaler
    LSTM_AVAILABLE = True
except ImportError:
    LSTM_AVAILABLE = False
    print("Warning: tensorflow not installed. LSTM model will not be available.")


class LSTMModel:
    """LSTM Neural Network for cryptocurrency price forecasting"""
    
    def __init__(self, lookback: int = None, units: int = None):
        self.model = None
        self.scaler = MinMaxScaler(feature_range=(0, 1)) if LSTM_AVAILABLE else None
        self.lookback = lookback or config.LSTM_CONFIG['lookback']
        self.units = units or config.LSTM_CONFIG['units']
        self.train_data = None
        self.predictions = None
        self.model_name = "LSTM"
        self.last_sequence = None
        self.training_history = None
    
    def create_sequences(self, data: np.ndarray) -> tuple:
        """
        Create sequences for LSTM training
        
        Args:
            data: Scaled price data
        
        Returns:
            Tuple of (X, y) sequences
        """
        X, y = [], []
        for i in range(self.lookback, len(data)):
            X.append(data[i-self.lookback:i, 0])
            y.append(data[i, 0])
        return np.array(X), np.array(y)
    
    def build_model(self, input_shape: tuple) -> Sequential:
        """
        Build LSTM model architecture
        
        Args:
            input_shape: Shape of input data
        
        Returns:
            Compiled Keras model
        """
        model = Sequential([
            LSTM(self.units, return_sequences=True, input_shape=input_shape),
            Dropout(0.2),
            LSTM(self.units, return_sequences=False),
            Dropout(0.2),
            Dense(25),
            Dense(1)
        ])
        
        model.compile(optimizer='adam', loss='mean_squared_error')
        return model
    
    def fit(self, series: pd.Series, epochs: int = None, batch_size: int = None,
            validation_split: float = None):
        """
        Fit LSTM model
        
        Args:
            series: Price series
            epochs: Training epochs
            batch_size: Batch size
            validation_split: Validation data fraction
        """
        if not LSTM_AVAILABLE:
            raise ImportError("tensorflow is required for LSTM model")
        
        epochs = epochs or config.LSTM_CONFIG['epochs']
        batch_size = batch_size or config.LSTM_CONFIG['batch_size']
        validation_split = validation_split or config.LSTM_CONFIG['validation_split']
        
        self.train_data = series.copy()
        
        print(f"Fitting LSTM model (lookback={self.lookback}, units={self.units})...")
        
        # Prepare data
        data = series.values.reshape(-1, 1)
        scaled_data = self.scaler.fit_transform(data)
        
        # Create sequences
        X, y = self.create_sequences(scaled_data)
        
        # Reshape for LSTM [samples, time steps, features]
        X = X.reshape((X.shape[0], X.shape[1], 1))
        
        # Build model
        self.model = self.build_model((X.shape[1], 1))
        
        # Early stopping callback
        early_stop = EarlyStopping(
            monitor='val_loss',
            patience=10,
            restore_best_weights=True
        )
        
        # Train model
        self.training_history = self.model.fit(
            X, y,
            epochs=epochs,
            batch_size=batch_size,
            validation_split=validation_split,
            callbacks=[early_stop],
            verbose=1
        )
        
        # Store last sequence for prediction
        self.last_sequence = scaled_data[-self.lookback:]
        
        print("Model fitted successfully")
    
    def predict(self, horizon: int = 7) -> pd.DataFrame:
        """
        Generate multi-step forecasts
        
        Args:
            horizon: Number of days to forecast
        
        Returns:
            DataFrame with forecasts
        """
        if self.model is None:
            raise ValueError("Model must be fitted before prediction")
        
        print(f"Generating {horizon}-day forecast...")
        
        predictions = []
        current_sequence = self.last_sequence.copy()
        
        for _ in range(horizon):
            # Reshape for prediction
            X_pred = current_sequence.reshape((1, self.lookback, 1))
            
            # Predict next value
            pred = self.model.predict(X_pred, verbose=0)
            predictions.append(pred[0, 0])
            
            # Update sequence
            current_sequence = np.roll(current_sequence, -1)
            current_sequence[-1] = pred[0, 0]
        
        # Inverse transform predictions
        predictions = np.array(predictions).reshape(-1, 1)
        predictions = self.scaler.inverse_transform(predictions)
        
        # Calculate confidence intervals (approximate using training std)
        train_std = self.train_data.std() * 0.1  # 10% of historical std as uncertainty
        
        # Create date index for forecast
        last_date = self.train_data.index[-1] if hasattr(self.train_data, 'index') and \
                    isinstance(self.train_data.index[-1], datetime) else datetime.now()
        forecast_dates = pd.date_range(start=last_date + timedelta(days=1), periods=horizon, freq='D')
        
        # Create forecast DataFrame
        result = pd.DataFrame({
            'date': forecast_dates,
            'forecast': predictions.flatten(),
            'lower_ci': predictions.flatten() - 1.96 * train_std,
            'upper_ci': predictions.flatten() + 1.96 * train_std
        })
        
        self.predictions = result
        return result
    
    def get_training_history(self) -> dict:
        """Get training history"""
        if self.training_history is None:
            return {}
        
        return {
            'loss': self.training_history.history['loss'],
            'val_loss': self.training_history.history.get('val_loss', [])
        }
    
    def get_metrics(self) -> dict:
        """Get model metrics"""
        history = self.get_training_history()
        
        return {
            'lookback': self.lookback,
            'units': self.units,
            'final_loss': history['loss'][-1] if history.get('loss') else None,
            'final_val_loss': history['val_loss'][-1] if history.get('val_loss') else None
        }
    
    def save_model(self, filepath: str = None):
        """Save fitted model to file"""
        if filepath is None:
            filepath = os.path.join(config.MODELS_DIR, 'lstm_model')
        
        # Save Keras model
        self.model.save(filepath + '.keras')
        
        # Save scaler and other attributes
        with open(filepath + '_meta.pkl', 'wb') as f:
            pickle.dump({
                'scaler': self.scaler,
                'lookback': self.lookback,
                'units': self.units,
                'last_sequence': self.last_sequence,
                'train_data': self.train_data
            }, f)
        print(f"Model saved to {filepath}")
    
    def load_model(self, filepath: str = None):
        """Load fitted model from file"""
        if filepath is None:
            filepath = os.path.join(config.MODELS_DIR, 'lstm_model')
        
        # Load Keras model
        self.model = load_model(filepath + '.keras')
        
        # Load metadata
        with open(filepath + '_meta.pkl', 'rb') as f:
            data = pickle.load(f)
            self.scaler = data['scaler']
            self.lookback = data['lookback']
            self.units = data['units']
            self.last_sequence = data['last_sequence']
            self.train_data = data['train_data']
        print(f"Model loaded from {filepath}")


def train_lstm(series: pd.Series, horizon: int = 7, lookback: int = 60) -> pd.DataFrame:
    """
    Convenience function to train LSTM and get forecasts
    
    Args:
        series: Price series
        horizon: Forecast horizon in days
        lookback: Number of lookback days
    
    Returns:
        DataFrame with forecasts
    """
    model = LSTMModel(lookback=lookback)
    model.fit(series)
    predictions = model.predict(horizon)
    return predictions


if __name__ == "__main__":
    # Test LSTM model
    print("Testing LSTM model...")
    
    # Create sample data
    np.random.seed(42)
    dates = pd.date_range(start='2023-01-01', periods=200, freq='D')
    prices = 50000 + np.cumsum(np.random.randn(200) * 500)
    series = pd.Series(prices, index=dates)
    
    # Train and predict (using smaller epochs for testing)
    model = LSTMModel(lookback=30, units=32)
    model.fit(series, epochs=10)
    forecast = model.predict(horizon=7)
    
    print("\nForecast:")
    print(forecast)
    print("\nMetrics:", model.get_metrics())
