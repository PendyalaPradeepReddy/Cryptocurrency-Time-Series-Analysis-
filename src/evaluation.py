"""
Model Evaluation Module - Compare and evaluate forecasting models
"""
import os
import sys
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config


def calculate_mape(actual: np.ndarray, predicted: np.ndarray) -> float:
    """
    Calculate Mean Absolute Percentage Error
    
    Args:
        actual: Actual values
        predicted: Predicted values
    
    Returns:
        MAPE as percentage
    """
    actual = np.array(actual)
    predicted = np.array(predicted)
    
    # Avoid division by zero
    mask = actual != 0
    mape = np.mean(np.abs((actual[mask] - predicted[mask]) / actual[mask])) * 100
    
    return mape


def calculate_rmse(actual: np.ndarray, predicted: np.ndarray) -> float:
    """
    Calculate Root Mean Squared Error
    
    Args:
        actual: Actual values
        predicted: Predicted values
    
    Returns:
        RMSE value
    """
    actual = np.array(actual)
    predicted = np.array(predicted)
    
    rmse = np.sqrt(np.mean((actual - predicted) ** 2))
    return rmse


def calculate_mae(actual: np.ndarray, predicted: np.ndarray) -> float:
    """
    Calculate Mean Absolute Error
    
    Args:
        actual: Actual values
        predicted: Predicted values
    
    Returns:
        MAE value
    """
    actual = np.array(actual)
    predicted = np.array(predicted)
    
    mae = np.mean(np.abs(actual - predicted))
    return mae


def calculate_r2(actual: np.ndarray, predicted: np.ndarray) -> float:
    """
    Calculate R-squared (coefficient of determination)
    
    Args:
        actual: Actual values
        predicted: Predicted values
    
    Returns:
        R2 score
    """
    actual = np.array(actual)
    predicted = np.array(predicted)
    
    ss_res = np.sum((actual - predicted) ** 2)
    ss_tot = np.sum((actual - np.mean(actual)) ** 2)
    
    r2 = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0
    return r2


def evaluate_model(actual: np.ndarray, predicted: np.ndarray, model_name: str = "Model") -> dict:
    """
    Comprehensive model evaluation
    
    Args:
        actual: Actual values
        predicted: Predicted values
        model_name: Name of the model
    
    Returns:
        Dictionary with all metrics
    """
    metrics = {
        'model': model_name,
        'mape': calculate_mape(actual, predicted),
        'rmse': calculate_rmse(actual, predicted),
        'mae': calculate_mae(actual, predicted),
        'r2': calculate_r2(actual, predicted)
    }
    
    return metrics


def compare_models(results: list) -> pd.DataFrame:
    """
    Compare multiple models' performance
    
    Args:
        results: List of dictionaries with model metrics
    
    Returns:
        Comparison DataFrame
    """
    comparison = pd.DataFrame(results)
    comparison = comparison.sort_values('mape', ascending=True)
    comparison = comparison.reset_index(drop=True)
    
    # Add ranking
    comparison['rank'] = range(1, len(comparison) + 1)
    
    return comparison


def create_comparison_chart(comparison_df: pd.DataFrame) -> go.Figure:
    """
    Create model comparison bar chart
    
    Args:
        comparison_df: DataFrame with model metrics
    
    Returns:
        Plotly Figure
    """
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('MAPE (%)', 'RMSE', 'MAE', 'R² Score'),
        specs=[[{"type": "bar"}, {"type": "bar"}],
               [{"type": "bar"}, {"type": "bar"}]]
    )
    
    colors = ['#00D4FF', '#FFD700', '#FF6B6B', '#00FF88']
    
    # MAPE
    fig.add_trace(go.Bar(
        x=comparison_df['model'],
        y=comparison_df['mape'],
        name='MAPE',
        marker_color=colors[0]
    ), row=1, col=1)
    
    # RMSE
    fig.add_trace(go.Bar(
        x=comparison_df['model'],
        y=comparison_df['rmse'],
        name='RMSE',
        marker_color=colors[1]
    ), row=1, col=2)
    
    # MAE
    fig.add_trace(go.Bar(
        x=comparison_df['model'],
        y=comparison_df['mae'],
        name='MAE',
        marker_color=colors[2]
    ), row=2, col=1)
    
    # R2
    fig.add_trace(go.Bar(
        x=comparison_df['model'],
        y=comparison_df['r2'],
        name='R²',
        marker_color=colors[3]
    ), row=2, col=2)
    
    fig.update_layout(
        title='Model Performance Comparison',
        template='plotly_dark',
        showlegend=False,
        height=600
    )
    
    return fig


def create_forecast_comparison_chart(forecasts: dict, actual: pd.DataFrame = None) -> go.Figure:
    """
    Create comparison chart of all model forecasts
    
    Args:
        forecasts: Dictionary mapping model names to forecast DataFrames
        actual: Optional actual values for comparison
    
    Returns:
        Plotly Figure
    """
    fig = go.Figure()
    
    colors = {
        'ARIMA': '#00D4FF',
        'SARIMA': '#FFD700',
        'Prophet': '#FF6B6B',
        'LSTM': '#00FF88'
    }
    
    for model_name, forecast_df in forecasts.items():
        color = colors.get(model_name, '#FFFFFF')
        
        # Add forecast line
        fig.add_trace(go.Scatter(
            x=forecast_df['date'],
            y=forecast_df['forecast'],
            name=model_name,
            line=dict(color=color, width=2)
        ))
        
        # Add confidence interval
        if 'lower_ci' in forecast_df.columns and 'upper_ci' in forecast_df.columns:
            fig.add_trace(go.Scatter(
                x=pd.concat([forecast_df['date'], forecast_df['date'][::-1]]),
                y=pd.concat([forecast_df['upper_ci'], forecast_df['lower_ci'][::-1]]),
                fill='toself',
                fillcolor=f"rgba{tuple(list(int(color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4)) + [0.2])}",
                line=dict(color='rgba(255,255,255,0)'),
                showlegend=False,
                name=f'{model_name} CI'
            ))
    
    # Add actual values if provided
    if actual is not None:
        fig.add_trace(go.Scatter(
            x=actual['date'],
            y=actual['close'],
            name='Actual',
            line=dict(color='white', width=2, dash='dot')
        ))
    
    fig.update_layout(
        title='Forecast Comparison',
        xaxis_title='Date',
        yaxis_title='Price (USD)',
        template='plotly_dark',
        hovermode='x unified',
        legend=dict(orientation="h", yanchor="bottom", y=1.02)
    )
    
    return fig


def create_residuals_chart(actual: np.ndarray, predicted: np.ndarray, 
                           model_name: str = "Model") -> go.Figure:
    """
    Create residuals analysis chart
    
    Args:
        actual: Actual values
        predicted: Predicted values
        model_name: Name of the model
    
    Returns:
        Plotly Figure
    """
    residuals = np.array(actual) - np.array(predicted)
    
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('Residuals Over Time', 'Residuals Distribution')
    )
    
    # Residuals over time
    fig.add_trace(go.Scatter(
        y=residuals,
        mode='markers',
        marker=dict(color='#00D4FF', size=5),
        name='Residuals'
    ), row=1, col=1)
    
    # Add zero line
    fig.add_hline(y=0, line_dash="dash", line_color="red", row=1, col=1)
    
    # Residuals histogram
    fig.add_trace(go.Histogram(
        x=residuals,
        nbinsx=30,
        marker_color='#00D4FF',
        opacity=0.7,
        name='Distribution'
    ), row=1, col=2)
    
    fig.update_layout(
        title=f'{model_name} Residuals Analysis',
        template='plotly_dark',
        showlegend=False,
        height=400
    )
    
    return fig


def rolling_window_cv(series: pd.Series, model_class, window_size: int = 100,
                      horizon: int = 7, step: int = 30) -> list:
    """
    Perform rolling window cross-validation
    
    Args:
        series: Time series data
        model_class: Model class to evaluate
        window_size: Training window size
        horizon: Forecast horizon
        step: Step size between windows
    
    Returns:
        List of evaluation results
    """
    results = []
    
    for i in range(0, len(series) - window_size - horizon, step):
        # Training data
        train = series.iloc[i:i + window_size]
        
        # Test data
        test = series.iloc[i + window_size:i + window_size + horizon]
        
        try:
            # Fit and predict
            model = model_class()
            model.fit(train)
            forecast = model.predict(horizon)
            
            # Evaluate
            metrics = evaluate_model(
                test.values,
                forecast['forecast'].values,
                model_class.__name__
            )
            metrics['fold'] = len(results) + 1
            results.append(metrics)
            
        except Exception as e:
            print(f"Fold {len(results) + 1} failed: {e}")
            continue
    
    return results


def get_best_model(comparison_df: pd.DataFrame, metric: str = 'mape') -> str:
    """
    Get the best performing model based on a metric
    
    Args:
        comparison_df: Model comparison DataFrame
        metric: Metric to use for selection
    
    Returns:
        Name of best model
    """
    if metric in ['mape', 'rmse', 'mae']:
        best_idx = comparison_df[metric].idxmin()
    else:  # r2 - higher is better
        best_idx = comparison_df[metric].idxmax()
    
    return comparison_df.loc[best_idx, 'model']


if __name__ == "__main__":
    # Test evaluation functions
    print("Testing evaluation module...")
    
    # Create sample data
    np.random.seed(42)
    actual = np.linspace(50000, 55000, 30) + np.random.randn(30) * 500
    predicted = actual + np.random.randn(30) * 300  # Add some error
    
    # Evaluate
    metrics = evaluate_model(actual, predicted, "Test Model")
    print(f"\nMetrics: {metrics}")
    
    # Test comparison
    results = [
        evaluate_model(actual, predicted + np.random.randn(30) * 200, "ARIMA"),
        evaluate_model(actual, predicted + np.random.randn(30) * 180, "SARIMA"),
        evaluate_model(actual, predicted + np.random.randn(30) * 150, "Prophet"),
        evaluate_model(actual, predicted + np.random.randn(30) * 250, "LSTM")
    ]
    
    comparison = compare_models(results)
    print(f"\nModel Comparison:\n{comparison}")
    print(f"\nBest Model: {get_best_model(comparison)}")
