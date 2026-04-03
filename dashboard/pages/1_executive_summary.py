"""
Executive Summary Page - Dashboard Overview
"""
import os
import sys

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta

import config
from src.data_loader import load_coin_data, get_available_symbols

st.set_page_config(page_title="Executive Summary", page_icon="📊", layout="wide")

st.markdown("# 📊 Executive Summary")
st.markdown("High-level overview of cryptocurrency market performance")


def load_all_data():
    """Load data for all available coins"""
    data = {}
    available_symbols = [s for s in get_available_symbols() if s in config.CRYPTO_LIST]
    
    for symbol in available_symbols[:6]:  # Limit to first 6 for performance
        try:
            df = load_coin_data(symbol)
            data[symbol] = df
        except Exception as e:
            st.warning(f"Error loading {symbol}: {e}")
    return data


def create_sparkline(df: pd.DataFrame, days: int = 30) -> go.Figure:
    """Create mini sparkline chart"""
    recent = df.tail(min(days, len(df)))
    
    color = '#00FF88' if recent['close'].iloc[-1] >= recent['close'].iloc[0] else '#FF4444'
    
    fig = go.Figure(go.Scatter(
        x=recent['date'],
        y=recent['close'],
        mode='lines',
        line=dict(color=color, width=2),
        fill='tozeroy',
        fillcolor=f"rgba{tuple(list(int(color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4)) + [0.1])}"
    ))
    
    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        height=80,
        showlegend=False,
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig


def main():
    # Load data
    with st.spinner("Loading cryptocurrency data..."):
        try:
            data = load_all_data()
        except FileNotFoundError as e:
            st.error(f"❌ Failed to load data: {str(e)}")
            with st.expander("Debug Info"):
                st.write(f"Project root: {config.BASE_DIR}")
                st.write(f"Data file path: {config.DATA_FILE}")
                st.write(f"Data file exists: {os.path.exists(config.DATA_FILE)}")
            return
    
    if not data:
        st.warning("⚠️ No data could be loaded. Please check that main_df_enhanced.csv exists and contains data.")
        with st.expander("Troubleshooting"):
            st.write(f"**Data file location:** {config.DATA_FILE}")
            st.write(f"**File exists:** {os.path.exists(config.DATA_FILE)}")
            if os.path.exists(config.DATA_FILE):
                df_test = pd.read_csv(config.DATA_FILE)
                st.write(f"**File has {len(df_test)} rows**")
        return
    
    # Market Overview Cards
    st.markdown("### 🪙 Market Overview")
    
    cols = st.columns(min(len(data), 4))
    
    for i, (symbol, df) in enumerate(list(data.items())[:4]):
        with cols[i]:
            coin_info = config.CRYPTO_LIST.get(symbol, {"symbol": symbol, "name": symbol})
            current_price = df['close'].iloc[-1]
            price_change_24h = ((df['close'].iloc[-1] / df['close'].iloc[-2]) - 1) * 100 if len(df) > 1 else 0
            
            st.metric(
                label=f"{coin_info['symbol']}",
                value=f"${current_price:,.2f}",
                delta=f"{price_change_24h:+.2f}%"
            )
            
            # Sparkline
            sparkline = create_sparkline(df, 30)
            st.plotly_chart(sparkline, use_container_width=True, config={'displayModeBar': False})
    
    st.markdown("---")
    
    # Performance Summary
    st.markdown("### 📈 Performance Summary")
    
    perf_data = []
    for symbol, df in data.items():
        coin_info = config.CRYPTO_LIST.get(symbol, {"symbol": symbol, "name": symbol})
        
        perf_data.append({
            'Coin': coin_info['symbol'],
            'Current Price': f"${df['close'].iloc[-1]:,.2f}",
            'Return': f"{((df['close'].iloc[-1] / df['close'].iloc[0]) - 1) * 100:+.2f}%",
            'High': f"${df['close'].max():,.2f}",
            'Low': f"${df['close'].min():,.2f}",
            'Volatility': f"{df['close'].pct_change().std() * np.sqrt(365) * 100:.2f}%"
        })
    
    perf_df = pd.DataFrame(perf_data)
    st.dataframe(perf_df, use_container_width=True, hide_index=True)
    
    # Comparison Chart
    st.markdown("---")
    st.markdown("### 🔄 Normalized Performance Comparison")
    
    fig = go.Figure()
    colors = ['#00D4FF', '#FFD700', '#FF6B6B', '#00FF88', '#9B59B6', '#E74C3C']
    
    for i, (symbol, df) in enumerate(data.items()):
        normalized = (df['close'] / df['close'].iloc[0]) * 100
        
        fig.add_trace(go.Scatter(
            x=df['date'],
            y=normalized,
            name=symbol,
            line=dict(color=colors[i % len(colors)], width=2)
        ))
    
    fig.update_layout(
        title='Normalized Performance (Base = 100)',
        xaxis_title='Date',
        yaxis_title='Normalized Price',
        template='plotly_dark',
        hovermode='x unified',
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)


if __name__ == "__main__":
    main()
