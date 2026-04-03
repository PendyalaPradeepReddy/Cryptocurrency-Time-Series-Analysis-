"""
Crypto Analytics Dashboard - Main Entry Point
Interactive dashboard for cryptocurrency time series analysis and forecasting
"""
import os
import sys

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.graph_objects as go

import config
from src.data_loader import load_coin_data, load_main_data, get_available_symbols
from src.eda import (
    create_price_chart, create_volatility_chart, create_returns_distribution,
    create_correlation_heatmap, create_bollinger_bands_chart, create_rsi_chart,
    create_multi_coin_comparison, generate_statistical_summary
)

# Page config
st.set_page_config(
    page_title=config.DASHBOARD_TITLE,
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark theme styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        background: linear-gradient(90deg, #00D4FF, #FFD700);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 1rem 0;
    }
    .metric-card {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        padding: 1.5rem;
        border-radius: 15px;
        border: 1px solid #00D4FF33;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
    .stMetric {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #00D4FF22;
    }
    div[data-testid="stSidebarContent"] {
        background: linear-gradient(180deg, #0f0f23 0%, #1a1a2e 100%);
    }
</style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize session state variables"""
    if 'data_loaded' not in st.session_state:
        st.session_state.data_loaded = False
    if 'processed_data' not in st.session_state:
        st.session_state.processed_data = {}


def load_all_coin_data():
    """Load data for all available coins from main_df_enhanced.csv"""
    data_dict = {}
    available_symbols = get_available_symbols()
    
    for symbol in available_symbols:
        if symbol in config.CRYPTO_LIST:
            try:
                df = load_coin_data(symbol)
                data_dict[symbol] = df
            except Exception as e:
                st.warning(f"Error loading {symbol}: {e}")
    
    return data_dict


def sidebar_controls():
    """Create sidebar with controls"""
    st.sidebar.markdown("## 🎛️ Controls")
    
    # Get available symbols
    available_symbols = [s for s in get_available_symbols() if s in config.CRYPTO_LIST]
    
    # Coin selection
    selected_coin = st.sidebar.selectbox(
        "Select Cryptocurrency",
        options=available_symbols,
        format_func=lambda x: f"{x} - {config.CRYPTO_LIST.get(x, {}).get('name', x)}",
        index=0
    )
    
    # Data reload button
    st.sidebar.markdown("### 🔄 Data Management")
    
    if st.sidebar.button("🔃 Reload Data", use_container_width=True):
        with st.spinner("Reloading data..."):
            st.session_state.processed_data = load_all_coin_data()
            st.session_state.data_loaded = True
            st.success("Data reloaded!")
            st.rerun()
    
    # Data info
    if st.session_state.data_loaded:
        st.sidebar.success(f"✅ {len(st.session_state.processed_data)} coins loaded")
    
    return selected_coin


def display_kpis(df: pd.DataFrame, coin_name: str):
    """Display key performance indicators"""
    col1, col2, col3, col4 = st.columns(4)
    
    current_price = df['close'].iloc[-1]
    prev_price = df['close'].iloc[-2] if len(df) > 1 else current_price
    price_change = (current_price - prev_price) / prev_price * 100
    
    with col1:
        st.metric(
            label=f"💰 {coin_name} Price",
            value=f"${current_price:,.2f}",
            delta=f"{price_change:.2f}%"
        )
    
    with col2:
        vol_24h = df['volume'].iloc[-1] if 'volume' in df.columns else 0
        st.metric(
            label="📊 Volume",
            value=f"${vol_24h/1e6:.2f}M" if vol_24h > 1e6 else f"${vol_24h:,.0f}"
        )
    
    with col3:
        if 'volatility_30' in df.columns:
            volatility = df['volatility_30'].iloc[-1] * 100
        else:
            volatility = df['close'].pct_change().rolling(30).std().iloc[-1] * 100
        st.metric(
            label="📈 30d Volatility",
            value=f"{volatility:.2f}%"
        )
    
    with col4:
        total_return = (df['close'].iloc[-1] / df['close'].iloc[0] - 1) * 100
        st.metric(
            label="📉 Total Return",
            value=f"{total_return:.2f}%"
        )
    
    # Sentiment if available
    if 'sentiment' in df.columns:
        avg_sentiment = df['sentiment'].iloc[-1]
        sentiment_label = "🟢 Positive" if avg_sentiment > 50 else "🔴 Negative" if avg_sentiment < 50 else "🟡 Neutral"
        st.sidebar.metric("Sentiment", sentiment_label, f"Score: {avg_sentiment}")


def main_content(coin_id: str):
    """Display main dashboard content"""
    # Load data if not in session state
    if coin_id not in st.session_state.processed_data:
        try:
            st.session_state.processed_data[coin_id] = load_coin_data(coin_id)
        except Exception as e:
            st.error(f"Error loading {coin_id}: {e}")
            return
    
    df = st.session_state.processed_data[coin_id]
    coin_info = config.CRYPTO_LIST.get(coin_id, {"symbol": coin_id, "name": coin_id})
    coin_name = coin_info['name']
    
    if df.empty:
        st.warning("No data available.")
        return
    
    # KPIs
    display_kpis(df, coin_name)
    
    st.markdown("---")
    
    # Price Chart
    st.markdown("### 📈 Price History")
    price_chart = create_price_chart(df, coin_name)
    st.plotly_chart(price_chart, use_container_width=True)
    
    # Two column layout
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Volatility Analysis")
        vol_chart = create_volatility_chart(df, coin_name)
        st.plotly_chart(vol_chart, use_container_width=True)
    
    with col2:
        st.markdown("### 📉 Returns Distribution")
        returns_chart = create_returns_distribution(df, coin_name)
        st.plotly_chart(returns_chart, use_container_width=True)
    
    # Technical Indicators
    st.markdown("---")
    st.markdown("### 🔧 Technical Indicators")
    
    tab1, tab2 = st.tabs(["Bollinger Bands", "RSI"])
    
    with tab1:
        if 'bb_upper' in df.columns:
            bb_chart = create_bollinger_bands_chart(df, coin_name)
            st.plotly_chart(bb_chart, use_container_width=True)
        else:
            st.info("Bollinger Bands data not available.")
    
    with tab2:
        if 'rsi' in df.columns:
            rsi_chart = create_rsi_chart(df, coin_name)
            st.plotly_chart(rsi_chart, use_container_width=True)
        else:
            st.info("RSI data not available.")
    
    # Multi-coin comparison
    if len(st.session_state.processed_data) > 1:
        st.markdown("---")
        st.markdown("### 🔄 Multi-Coin Comparison")
        
        # Select coins to compare
        compare_coins = st.multiselect(
            "Select coins to compare",
            options=list(st.session_state.processed_data.keys()),
            default=list(st.session_state.processed_data.keys())[:3]
        )
        
        if compare_coins and len(compare_coins) > 1:
            filtered_data = {k: st.session_state.processed_data[k] for k in compare_coins 
                          if k in st.session_state.processed_data}
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                comparison_chart = create_multi_coin_comparison(filtered_data)
                st.plotly_chart(comparison_chart, use_container_width=True)
            
            with col2:
                corr_chart = create_correlation_heatmap(filtered_data)
                st.plotly_chart(corr_chart, use_container_width=True)
    
    # Statistics table
    st.markdown("---")
    st.markdown("### 📋 Statistical Summary")
    stats_df = generate_statistical_summary(df)
    st.dataframe(stats_df, use_container_width=True, hide_index=True)


def main():
    """Main dashboard function"""
    # Initialize
    initialize_session_state()
    
    # Load data on first run
    if not st.session_state.data_loaded:
        with st.spinner("Loading cryptocurrency data..."):
            try:
                st.session_state.processed_data = load_all_coin_data()
                st.session_state.data_loaded = True
            except FileNotFoundError as e:
                st.session_state.data_loaded = False
                st.session_state.processed_data = {}
    
    # Header
    st.markdown('<h1 class="main-header">📊 Crypto Analytics Dashboard</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #888;">Real-time cryptocurrency analysis and forecasting</p>', unsafe_allow_html=True)
    
    # Sidebar
    try:
        selected_coin = sidebar_controls()
    except FileNotFoundError as e:
        st.error(f"❌ Failed to load data!\n\n{str(e)}")
        st.info("**Troubleshooting:**\n- Ensure main_df_enhanced.csv exists in the project root\n- Check file permissions\n- Verify the app is running from the correct directory")
        return
    
    # Main content
    if st.session_state.processed_data:
        main_content(selected_coin)
    else:
        st.error(f"Failed to load data. Please check that main_df_enhanced.csv exists.")
        with st.expander("Debug Info"):
            st.write(f"Project root: {config.BASE_DIR}")
            st.write(f"Data file path: {config.DATA_FILE}")
            st.write(f"Data file exists: {os.path.exists(config.DATA_FILE)}")
            st.write(f"Current working directory: {os.getcwd()}")
            st.write(f"Data directory: {config.DATA_DIR}")
            st.write(f"Data directory contents: {os.listdir(config.DATA_DIR) if os.path.exists(config.DATA_DIR) else 'Not found'}")


if __name__ == "__main__":
    main()
