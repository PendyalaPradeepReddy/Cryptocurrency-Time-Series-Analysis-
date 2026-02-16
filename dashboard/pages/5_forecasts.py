"""
Forecasts Page - Generate and view price forecasts
"""
import os
import sys

project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import warnings
warnings.filterwarnings('ignore')

import config
from src.data_loader import load_coin_data, get_available_symbols

st.set_page_config(page_title="Forecasts", page_icon="🔮", layout="wide")

st.markdown("# 🔮 Price Forecasts")
st.markdown("Generate price predictions using different models")


def generate_forecast(df: pd.DataFrame, model_name: str, horizon: int) -> pd.DataFrame:
    """Generate forecast using selected model"""
    train_series = df.set_index('date')['close']
    
    if model_name == "ARIMA":
        from src.models.arima_model import ARIMAModel
        model = ARIMAModel()
        model.fit(train_series, order=(2, 1, 2))
        return model.predict(horizon)
        
    elif model_name == "SARIMA":
        from src.models.sarima_model import SARIMAModel
        model = SARIMAModel(seasonal_period=7)
        model.fit(train_series, order=(1, 1, 1), seasonal_order=(1, 0, 1, 7))
        return model.predict(horizon)
        
    elif model_name == "Prophet":
        from src.models.prophet_model import ProphetModel
        model = ProphetModel()
        model.fit(df, date_col='date', value_col='close')
        return model.predict(horizon)


def main():
    available_symbols = [s for s in get_available_symbols() if s in config.CRYPTO_LIST]
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        coin_id = st.selectbox("Select Coin", options=available_symbols,
            format_func=lambda x: f"{x} - {config.CRYPTO_LIST.get(x, {}).get('name', x)}")
    
    with col2:
        model_name = st.selectbox("Forecasting Model", options=["ARIMA", "SARIMA", "Prophet"], index=2)
    
    with col3:
        horizon = st.selectbox("Forecast Horizon", options=[7, 14, 30],
            format_func=lambda x: f"{x} days", index=0)
    
    # Load data
    try:
        with st.spinner(f"Loading {coin_id} data..."):
            df = load_coin_data(coin_id)
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return
    
    coin_name = config.CRYPTO_LIST.get(coin_id, {}).get('name', coin_id)
    current_price = df['close'].iloc[-1]
    
    # Current price info
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    col1.metric("Current Price", f"${current_price:,.2f}")
    col2.metric("Data Points", f"{len(df)}")
    col3.metric("Volatility", f"{df['close'].pct_change().std() * np.sqrt(365) * 100:.2f}%")
    
    st.markdown("---")
    
    # Generate Forecast
    if st.button("🔮 Generate Forecast", use_container_width=True, type="primary"):
        with st.spinner(f"Training {model_name} and generating forecast..."):
            try:
                forecast = generate_forecast(df, model_name, horizon)
                st.session_state['current_forecast'] = forecast
                st.session_state['forecast_model'] = model_name
                st.session_state['forecast_coin'] = coin_id
                st.success(f"✅ {model_name} forecast generated!")
            except Exception as e:
                st.error(f"Error generating forecast: {str(e)}")
                return
    
    # Display forecast
    if ('current_forecast' in st.session_state and 
        st.session_state.get('forecast_coin') == coin_id and
        st.session_state.get('forecast_model') == model_name):
        
        forecast = st.session_state['current_forecast']
        
        st.markdown("### 📊 Forecast Summary")
        
        final_forecast = forecast['forecast'].iloc[-1]
        price_change = ((final_forecast / current_price) - 1) * 100
        
        col1, col2, col3 = st.columns(3)
        col1.metric(f"Predicted Price ({horizon}d)", f"${final_forecast:,.2f}", f"{price_change:+.2f}%")
        col2.metric("Forecast Range", f"${forecast['forecast'].min():,.2f} - ${forecast['forecast'].max():,.2f}")
        if 'lower_ci' in forecast.columns:
            col3.metric("95% Confidence", f"${forecast['lower_ci'].iloc[-1]:,.2f} - ${forecast['upper_ci'].iloc[-1]:,.2f}")
        
        # Forecast Chart
        st.markdown("### 📈 Forecast Visualization")
        
        hist_df = df.tail(100)
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(x=hist_df['date'], y=hist_df['close'],
            name='Historical', line=dict(color='#00D4FF', width=2)))
        
        fig.add_trace(go.Scatter(x=forecast['date'], y=forecast['forecast'],
            name='Forecast', line=dict(color='#00FF88', width=3), mode='lines+markers'))
        
        if 'lower_ci' in forecast.columns:
            fig.add_trace(go.Scatter(
                x=pd.concat([forecast['date'], forecast['date'][::-1]]),
                y=pd.concat([forecast['upper_ci'], forecast['lower_ci'][::-1]]),
                fill='toself', fillcolor='rgba(0, 255, 136, 0.2)',
                line=dict(color='rgba(255,255,255,0)'), name='95% CI'))
        
        # Add vertical line at forecast start using shape instead of vline
        last_hist_date = hist_df['date'].iloc[-1]
        fig.add_shape(type="line", x0=last_hist_date, x1=last_hist_date, y0=0, y1=1,
            yref="paper", line=dict(color="yellow", width=2, dash="dash"))
        fig.add_annotation(x=last_hist_date, y=1, yref="paper", text="Forecast Start",
            showarrow=False, yshift=10, font=dict(color="yellow"))
        
        fig.update_layout(title=f'{coin_id} Price Forecast ({model_name})',
            xaxis_title='Date', yaxis_title='Price (USD)',
            template='plotly_dark', hovermode='x unified', height=450)
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Forecast Table
        st.markdown("### 📋 Forecast Details")
        display_df = forecast.copy()
        display_df['cum_change'] = ((display_df['forecast'] / current_price) - 1) * 100
        st.dataframe(display_df.assign(date=display_df['date'].dt.strftime('%Y-%m-%d')),
            use_container_width=True, hide_index=True)
        
        st.warning("⚠️ **Disclaimer**: These forecasts are for educational purposes only.")
    else:
        st.info("👆 Click 'Generate Forecast' to create price predictions")


if __name__ == "__main__":
    main()
