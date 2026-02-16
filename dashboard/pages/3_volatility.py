"""
Volatility Analysis Page - Risk metrics and volatility visualization
"""
import os
import sys

project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import config
from src.data_loader import load_coin_data, get_available_symbols
from src.utils import calculate_var, calculate_max_drawdown, calculate_sharpe_ratio

st.set_page_config(page_title="Volatility Analysis", page_icon="📊", layout="wide")

st.markdown("# 📊 Volatility Analysis")
st.markdown("Risk metrics, volatility trends, and risk indicators")


def main():
    # Get available symbols
    available_symbols = [s for s in get_available_symbols() if s in config.CRYPTO_LIST]
    
    # Coin selector
    coin_id = st.selectbox(
        "Select Coin",
        options=available_symbols,
        format_func=lambda x: f"{x} - {config.CRYPTO_LIST.get(x, {}).get('name', x)}"
    )
    
    # Load data
    try:
        with st.spinner(f"Loading {coin_id} data..."):
            df = load_coin_data(coin_id)
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return
    
    coin_name = config.CRYPTO_LIST.get(coin_id, {}).get('name', coin_id)
    
    # Ensure returns exist
    if 'returns' not in df.columns:
        df['returns'] = df['close'].pct_change()
    
    returns = df['returns'].dropna()
    
    # Risk Metrics Cards
    st.markdown("---")
    st.markdown("### 🎯 Key Risk Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        vol_ann = returns.std() * np.sqrt(365) * 100
        st.metric("Annualized Volatility", f"{vol_ann:.2f}%")
    
    with col2:
        var_95 = np.percentile(returns, 5) * 100
        st.metric("VaR (95%)", f"{var_95:.2f}%")
    
    with col3:
        max_dd = calculate_max_drawdown(df['close']) * 100
        st.metric("Max Drawdown", f"{max_dd:.2f}%")
    
    with col4:
        sharpe = calculate_sharpe_ratio(returns)
        st.metric("Sharpe Ratio", f"{sharpe:.2f}")
    
    # Volatility Chart
    st.markdown("---")
    st.markdown("### 📈 Volatility Over Time")
    
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.1,
                        row_heights=[0.6, 0.4], subplot_titles=(f'{coin_name} Price', 'Rolling Volatility'))
    
    fig.add_trace(go.Scatter(x=df['date'], y=df['close'], line=dict(color='#00D4FF', width=2),
        name='Price'), row=1, col=1)
    
    # Rolling volatility
    rolling_vol = returns.rolling(21).std() * np.sqrt(365) * 100
    fig.add_trace(go.Scatter(x=df['date'], y=rolling_vol, line=dict(color='#FF6B6B', width=2),
        fill='tozeroy', fillcolor='rgba(255, 107, 107, 0.2)', name='21d Volatility'), row=2, col=1)
    
    fig.update_layout(template='plotly_dark', height=500, showlegend=True, hovermode='x unified')
    fig.update_yaxes(title_text="Price (USD)", row=1, col=1)
    fig.update_yaxes(title_text="Volatility (%)", row=2, col=1)
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Returns Distribution
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📉 Returns Distribution")
        returns_pct = returns * 100
        
        fig = go.Figure()
        fig.add_trace(go.Histogram(x=returns_pct, nbinsx=50, marker_color='#00D4FF', opacity=0.7))
        
        var_95 = np.percentile(returns_pct, 5)
        fig.add_vline(x=var_95, line_dash="dash", line_color="orange", annotation_text=f"VaR 95%: {var_95:.2f}%")
        
        fig.update_layout(title='Daily Returns Distribution', xaxis_title='Daily Return (%)',
            yaxis_title='Frequency', template='plotly_dark', height=350)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 📊 Drawdown Analysis")
        peak = df['close'].expanding().max()
        drawdown = ((df['close'] - peak) / peak) * 100
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df['date'], y=drawdown, fill='tozeroy',
            line=dict(color='#FF4444', width=1), fillcolor='rgba(255, 68, 68, 0.3)'))
        fig.update_layout(title='Drawdown Over Time', xaxis_title='Date',
            yaxis_title='Drawdown (%)', template='plotly_dark', height=350)
        st.plotly_chart(fig, use_container_width=True)
    
    # Risk Summary
    st.markdown("---")
    st.markdown("### 📋 Risk Summary Statistics")
    
    risk_stats = {
        'Metric': ['Mean Daily Return', 'Std Dev (Daily)', 'Volatility (Ann.)', 'VaR (95%)', 'Max Drawdown', 'Sharpe Ratio'],
        'Value': [
            f"{returns.mean() * 100:.4f}%",
            f"{returns.std() * 100:.4f}%",
            f"{returns.std() * np.sqrt(365) * 100:.2f}%",
            f"{np.percentile(returns, 5) * 100:.4f}%",
            f"{calculate_max_drawdown(df['close']) * 100:.2f}%",
            f"{calculate_sharpe_ratio(returns):.4f}"
        ]
    }
    st.dataframe(pd.DataFrame(risk_stats), use_container_width=True, hide_index=True)


if __name__ == "__main__":
    main()
