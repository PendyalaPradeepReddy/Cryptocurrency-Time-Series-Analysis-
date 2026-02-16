"""
Exploratory Data Analysis Module - Visualization and statistical analysis
"""
import os
import sys
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import seaborn as sns

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config


def create_price_chart(df: pd.DataFrame, coin_name: str = "Cryptocurrency") -> go.Figure:
    """
    Create interactive price chart with moving averages
    
    Args:
        df: Preprocessed DataFrame
        coin_name: Name of cryptocurrency
    
    Returns:
        Plotly Figure object
    """
    fig = go.Figure()
    
    # Price line
    fig.add_trace(go.Scatter(
        x=df['date'],
        y=df['close'],
        name='Price',
        line=dict(color='#00D4FF', width=2)
    ))
    
    # Moving averages
    if 'sma_7' in df.columns:
        fig.add_trace(go.Scatter(
            x=df['date'],
            y=df['sma_7'],
            name='7-day SMA',
            line=dict(color='#FFD700', width=1, dash='dot')
        ))
    
    if 'sma_30' in df.columns:
        fig.add_trace(go.Scatter(
            x=df['date'],
            y=df['sma_30'],
            name='30-day SMA',
            line=dict(color='#FF6B6B', width=1, dash='dash')
        ))
    
    fig.update_layout(
        title=f'{coin_name} Price History',
        xaxis_title='Date',
        yaxis_title='Price (USD)',
        template='plotly_dark',
        hovermode='x unified',
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    return fig


def create_candlestick_chart(df: pd.DataFrame, coin_name: str = "Cryptocurrency") -> go.Figure:
    """
    Create candlestick chart
    
    Args:
        df: DataFrame with OHLC data
        coin_name: Name of cryptocurrency
    
    Returns:
        Plotly Figure object
    """
    fig = go.Figure(data=[go.Candlestick(
        x=df['date'],
        open=df['open'],
        high=df['high'],
        low=df['low'],
        close=df['close'],
        increasing_line_color='#00FF88',
        decreasing_line_color='#FF4444'
    )])
    
    fig.update_layout(
        title=f'{coin_name} Candlestick Chart',
        xaxis_title='Date',
        yaxis_title='Price (USD)',
        template='plotly_dark',
        xaxis_rangeslider_visible=False
    )
    
    return fig


def create_volume_chart(df: pd.DataFrame, coin_name: str = "Cryptocurrency") -> go.Figure:
    """
    Create volume bar chart
    
    Args:
        df: DataFrame with volume data
        coin_name: Name of cryptocurrency
    
    Returns:
        Plotly Figure object
    """
    # Color bars based on price movement
    colors = ['#00FF88' if row['close'] >= row['open'] else '#FF4444' 
              for _, row in df.iterrows()]
    
    fig = go.Figure(data=[go.Bar(
        x=df['date'],
        y=df['volume'],
        marker_color=colors,
        opacity=0.7
    )])
    
    fig.update_layout(
        title=f'{coin_name} Trading Volume',
        xaxis_title='Date',
        yaxis_title='Volume (USD)',
        template='plotly_dark'
    )
    
    return fig


def create_volatility_chart(df: pd.DataFrame, coin_name: str = "Cryptocurrency") -> go.Figure:
    """
    Create volatility visualization
    
    Args:
        df: DataFrame with volatility data
        coin_name: Name of cryptocurrency
    
    Returns:
        Plotly Figure object
    """
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                        vertical_spacing=0.1,
                        subplot_titles=(f'{coin_name} Price', 'Rolling Volatility'))
    
    # Price
    fig.add_trace(go.Scatter(
        x=df['date'],
        y=df['close'],
        name='Price',
        line=dict(color='#00D4FF')
    ), row=1, col=1)
    
    # Volatility
    if 'volatility_21' in df.columns:
        fig.add_trace(go.Scatter(
            x=df['date'],
            y=df['volatility_21'] * 100,  # Convert to percentage
            name='21-day Volatility',
            line=dict(color='#FF6B6B'),
            fill='tozeroy',
            fillcolor='rgba(255, 107, 107, 0.2)'
        ), row=2, col=1)
    
    fig.update_layout(
        template='plotly_dark',
        hovermode='x unified',
        showlegend=True,
        height=600
    )
    
    fig.update_yaxes(title_text="Price (USD)", row=1, col=1)
    fig.update_yaxes(title_text="Volatility (%)", row=2, col=1)
    
    return fig


def create_returns_distribution(df: pd.DataFrame, coin_name: str = "Cryptocurrency") -> go.Figure:
    """
    Create histogram of daily returns
    
    Args:
        df: DataFrame with returns data
        coin_name: Name of cryptocurrency
    
    Returns:
        Plotly Figure object
    """
    returns = df['returns'].dropna() * 100  # Convert to percentage
    
    fig = go.Figure()
    
    fig.add_trace(go.Histogram(
        x=returns,
        nbinsx=50,
        marker_color='#00D4FF',
        opacity=0.7,
        name='Daily Returns'
    ))
    
    # Add mean line
    mean_return = returns.mean()
    fig.add_vline(x=mean_return, line_dash="dash", line_color="yellow",
                  annotation_text=f"Mean: {mean_return:.2f}%")
    
    fig.update_layout(
        title=f'{coin_name} Daily Returns Distribution',
        xaxis_title='Daily Return (%)',
        yaxis_title='Frequency',
        template='plotly_dark'
    )
    
    return fig


def create_correlation_heatmap(data_dict: dict) -> go.Figure:
    """
    Create correlation heatmap across multiple cryptocurrencies
    
    Args:
        data_dict: Dictionary mapping coin names to DataFrames
    
    Returns:
        Plotly Figure object
    """
    # Extract returns from each coin
    returns_df = pd.DataFrame()
    
    for coin_id, df in data_dict.items():
        if 'returns' in df.columns:
            # Use coin_id directly as it's already a symbol
            symbol = config.CRYPTO_LIST.get(coin_id, {}).get('symbol', coin_id)
            returns_df[symbol] = df.set_index('date')['returns']
    
    # Calculate correlation matrix
    corr_matrix = returns_df.corr()
    
    fig = go.Figure(data=go.Heatmap(
        z=corr_matrix.values,
        x=corr_matrix.columns,
        y=corr_matrix.index,
        colorscale='RdBu',
        zmid=0,
        text=np.round(corr_matrix.values, 2),
        texttemplate='%{text}',
        textfont={"size": 14}
    ))
    
    fig.update_layout(
        title='Cryptocurrency Returns Correlation',
        template='plotly_dark',
        width=500,
        height=500
    )
    
    return fig


def create_bollinger_bands_chart(df: pd.DataFrame, coin_name: str = "Cryptocurrency") -> go.Figure:
    """
    Create Bollinger Bands chart
    
    Args:
        df: DataFrame with Bollinger Bands data
        coin_name: Name of cryptocurrency
    
    Returns:
        Plotly Figure object
    """
    fig = go.Figure()
    
    # Upper band
    fig.add_trace(go.Scatter(
        x=df['date'],
        y=df['bb_upper'],
        name='Upper Band',
        line=dict(color='rgba(255, 107, 107, 0.5)', width=1)
    ))
    
    # Lower band
    fig.add_trace(go.Scatter(
        x=df['date'],
        y=df['bb_lower'],
        name='Lower Band',
        line=dict(color='rgba(255, 107, 107, 0.5)', width=1),
        fill='tonexty',
        fillcolor='rgba(255, 107, 107, 0.1)'
    ))
    
    # Price
    fig.add_trace(go.Scatter(
        x=df['date'],
        y=df['close'],
        name='Price',
        line=dict(color='#00D4FF', width=2)
    ))
    
    # Middle band (SMA)
    fig.add_trace(go.Scatter(
        x=df['date'],
        y=df['bb_middle'],
        name='SMA (Middle)',
        line=dict(color='#FFD700', width=1, dash='dot')
    ))
    
    fig.update_layout(
        title=f'{coin_name} Bollinger Bands',
        xaxis_title='Date',
        yaxis_title='Price (USD)',
        template='plotly_dark',
        hovermode='x unified'
    )
    
    return fig


def create_rsi_chart(df: pd.DataFrame, coin_name: str = "Cryptocurrency") -> go.Figure:
    """
    Create RSI indicator chart
    
    Args:
        df: DataFrame with RSI data
        coin_name: Name of cryptocurrency
    
    Returns:
        Plotly Figure object
    """
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                        vertical_spacing=0.1,
                        row_heights=[0.7, 0.3],
                        subplot_titles=(f'{coin_name} Price', 'RSI'))
    
    # Price
    fig.add_trace(go.Scatter(
        x=df['date'],
        y=df['close'],
        name='Price',
        line=dict(color='#00D4FF')
    ), row=1, col=1)
    
    # RSI
    if 'rsi' in df.columns:
        fig.add_trace(go.Scatter(
            x=df['date'],
            y=df['rsi'],
            name='RSI',
            line=dict(color='#9B59B6')
        ), row=2, col=1)
        
        # Overbought/Oversold lines
        fig.add_hline(y=70, line_dash="dash", line_color="red", row=2, col=1)
        fig.add_hline(y=30, line_dash="dash", line_color="green", row=2, col=1)
    
    fig.update_layout(
        template='plotly_dark',
        hovermode='x unified',
        height=600
    )
    
    fig.update_yaxes(title_text="Price (USD)", row=1, col=1)
    fig.update_yaxes(title_text="RSI", row=2, col=1, range=[0, 100])
    
    return fig


def create_macd_chart(df: pd.DataFrame, coin_name: str = "Cryptocurrency") -> go.Figure:
    """
    Create MACD indicator chart
    
    Args:
        df: DataFrame with MACD data
        coin_name: Name of cryptocurrency
    
    Returns:
        Plotly Figure object
    """
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                        vertical_spacing=0.1,
                        row_heights=[0.7, 0.3],
                        subplot_titles=(f'{coin_name} Price', 'MACD'))
    
    # Price
    fig.add_trace(go.Scatter(
        x=df['date'],
        y=df['close'],
        name='Price',
        line=dict(color='#00D4FF')
    ), row=1, col=1)
    
    # MACD components
    if 'macd' in df.columns:
        fig.add_trace(go.Scatter(
            x=df['date'],
            y=df['macd'],
            name='MACD',
            line=dict(color='#3498DB')
        ), row=2, col=1)
        
        fig.add_trace(go.Scatter(
            x=df['date'],
            y=df['macd_signal'],
            name='Signal',
            line=dict(color='#E74C3C')
        ), row=2, col=1)
        
        # Histogram
        colors = ['#00FF88' if val >= 0 else '#FF4444' for val in df['macd_histogram']]
        fig.add_trace(go.Bar(
            x=df['date'],
            y=df['macd_histogram'],
            name='Histogram',
            marker_color=colors
        ), row=2, col=1)
    
    fig.update_layout(
        template='plotly_dark',
        hovermode='x unified',
        height=600
    )
    
    return fig


def create_multi_coin_comparison(data_dict: dict) -> go.Figure:
    """
    Create normalized price comparison across coins
    
    Args:
        data_dict: Dictionary mapping coin IDs to DataFrames
    
    Returns:
        Plotly Figure object
    """
    fig = go.Figure()
    
    colors = ['#00D4FF', '#FFD700', '#FF6B6B', '#00FF88', '#9B59B6', '#E74C3C']
    
    for i, (coin_id, df) in enumerate(data_dict.items()):
        color = colors[i % len(colors)]
        # Normalize prices to start at 100
        normalized = (df['close'] / df['close'].iloc[0]) * 100
        
        # Use coin_id directly as it's already a symbol
        symbol = config.CRYPTO_LIST.get(coin_id, {}).get('symbol', coin_id)
        fig.add_trace(go.Scatter(
            x=df['date'],
            y=normalized,
            name=symbol,
            line=dict(color=color, width=2)
        ))
    
    fig.update_layout(
        title='Normalized Price Comparison (Base = 100)',
        xaxis_title='Date',
        yaxis_title='Normalized Price',
        template='plotly_dark',
        hovermode='x unified',
        legend=dict(orientation="h", yanchor="bottom", y=1.02)
    )
    
    return fig


def generate_statistical_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate statistical summary table
    
    Args:
        df: Preprocessed DataFrame
    
    Returns:
        Summary DataFrame
    """
    summary = {
        'Metric': [
            'Current Price',
            'All-Time High',
            'All-Time Low',
            'Average Price',
            'Total Return',
            'Best Daily Return',
            'Worst Daily Return',
            'Avg Daily Return',
            'Volatility (30d)',
            'Sharpe Ratio',
            'Max Drawdown'
        ],
        'Value': [
            f"${df['close'].iloc[-1]:,.2f}",
            f"${df['close'].max():,.2f}",
            f"${df['close'].min():,.2f}",
            f"${df['close'].mean():,.2f}",
            f"{(df['close'].iloc[-1] / df['close'].iloc[0] - 1) * 100:.2f}%",
            f"{df['returns'].max() * 100:.2f}%" if 'returns' in df.columns else 'N/A',
            f"{df['returns'].min() * 100:.2f}%" if 'returns' in df.columns else 'N/A',
            f"{df['returns'].mean() * 100:.4f}%" if 'returns' in df.columns else 'N/A',
            f"{df['volatility_30'].iloc[-1] * 100:.2f}%" if 'volatility_30' in df.columns else 'N/A',
            f"{(df['returns'].mean() / df['returns'].std() * np.sqrt(365)):.2f}" if 'returns' in df.columns else 'N/A',
            f"{((df['close'] / df['close'].expanding().max() - 1).min()) * 100:.2f}%"
        ]
    }
    
    return pd.DataFrame(summary)


if __name__ == "__main__":
    # Test EDA functions
    print("Testing EDA module...")
    
    try:
        # Load processed data
        from src.preprocessing import load_processed_data
        
        btc_df = load_processed_data("bitcoin")
        
        # Generate charts
        print("\nGenerating charts...")
        price_chart = create_price_chart(btc_df, "Bitcoin")
        print("  - Price chart created")
        
        vol_chart = create_volatility_chart(btc_df, "Bitcoin")
        print("  - Volatility chart created")
        
        # Statistical summary
        summary = generate_statistical_summary(btc_df)
        print(f"\nStatistical Summary:\n{summary}")
        
    except Exception as e:
        print(f"Error: {e}")
