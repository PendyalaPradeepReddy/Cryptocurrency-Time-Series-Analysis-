"""
Price Trends Page - Detailed price analysis
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
from datetime import datetime, timedelta

import config
from src.data_loader import load_coin_data, get_available_symbols
from src.eda import create_price_chart, create_bollinger_bands_chart

st.set_page_config(page_title="Price Trends", page_icon="📈", layout="wide")

st.markdown("# 📈 Price Trends")
st.markdown("Detailed historical price analysis with technical indicators")


def main():
    # Get available symbols
    available_symbols = [s for s in get_available_symbols() if s in config.CRYPTO_LIST]
    
    # Coin selector
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
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
    
    with col2:
        # Time range filter
        max_rows = len(df)
        range_options = {"All": max_rows, "Last 500": min(500, max_rows), "Last 200": min(200, max_rows), "Last 100": min(100, max_rows)}
        time_range = st.selectbox("Data Range", options=list(range_options.keys()), index=0)
    
    df_filtered = df.tail(range_options[time_range])
    coin_name = config.CRYPTO_LIST.get(coin_id, {}).get('name', coin_id)
    
    # Price Statistics
    st.markdown("---")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Current Price",
            f"${df_filtered['close'].iloc[-1]:,.2f}",
            f"{((df_filtered['close'].iloc[-1] / df_filtered['close'].iloc[0]) - 1) * 100:+.2f}%"
        )
    
    with col2:
        st.metric("Period High", f"${df_filtered['close'].max():,.2f}")
    
    with col3:
        st.metric("Period Low", f"${df_filtered['close'].min():,.2f}")
    
    with col4:
        st.metric("Average Price", f"${df_filtered['close'].mean():,.2f}")
    
    # Chart
    st.markdown("---")
    
    chart_type = st.radio("Chart Type", options=["Line", "Candlestick", "With Indicators"], horizontal=True)
    
    if chart_type == "Line":
        fig = create_price_chart(df_filtered, coin_name)
        st.plotly_chart(fig, use_container_width=True)
        
    elif chart_type == "Candlestick":
        fig = go.Figure(data=[go.Candlestick(
            x=df_filtered['date'],
            open=df_filtered['open'],
            high=df_filtered['high'],
            low=df_filtered['low'],
            close=df_filtered['close'],
            increasing_line_color='#00FF88',
            decreasing_line_color='#FF4444'
        )])
        
        fig.update_layout(
            title=f'{coin_name} Candlestick Chart',
            template='plotly_dark',
            xaxis_rangeslider_visible=False,
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)
        
    else:  # With Indicators
        fig = make_subplots(
            rows=3, cols=1, shared_xaxes=True, vertical_spacing=0.05,
            row_heights=[0.5, 0.25, 0.25],
            subplot_titles=(f'{coin_name} Price with Bollinger Bands', 'RSI', 'Volume')
        )
        
        # Price with Bollinger Bands
        if 'bb_upper' in df_filtered.columns:
            fig.add_trace(go.Scatter(x=df_filtered['date'], y=df_filtered['bb_upper'],
                line=dict(color='rgba(255,107,107,0.5)', width=1), name='Upper BB'), row=1, col=1)
            fig.add_trace(go.Scatter(x=df_filtered['date'], y=df_filtered['bb_lower'],
                line=dict(color='rgba(255,107,107,0.5)', width=1), fill='tonexty',
                fillcolor='rgba(255,107,107,0.1)', name='Lower BB'), row=1, col=1)
        
        fig.add_trace(go.Scatter(x=df_filtered['date'], y=df_filtered['close'],
            line=dict(color='#00D4FF', width=2), name='Price'), row=1, col=1)
        
        # RSI
        if 'rsi' in df_filtered.columns:
            fig.add_trace(go.Scatter(x=df_filtered['date'], y=df_filtered['rsi'],
                line=dict(color='#9B59B6', width=1), name='RSI'), row=2, col=1)
            fig.add_hline(y=70, line_dash="dash", line_color="red", row=2, col=1)
            fig.add_hline(y=30, line_dash="dash", line_color="green", row=2, col=1)
        
        # Volume
        fig.add_trace(go.Bar(x=df_filtered['date'], y=df_filtered['volume'],
            marker_color='#00D4FF', opacity=0.7, name='Volume'), row=3, col=1)
        
        fig.update_layout(template='plotly_dark', height=700, showlegend=True)
        fig.update_yaxes(title_text="Price", row=1, col=1)
        fig.update_yaxes(title_text="RSI", range=[0, 100], row=2, col=1)
        fig.update_yaxes(title_text="Volume", row=3, col=1)
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Data Table
    st.markdown("---")
    with st.expander("📋 View Raw Data"):
        st.dataframe(df_filtered[['date', 'open', 'high', 'low', 'close', 'volume']].tail(30),
            use_container_width=True, hide_index=True)


if __name__ == "__main__":
    main()
