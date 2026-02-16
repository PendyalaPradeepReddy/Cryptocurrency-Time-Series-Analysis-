"""
Model Comparison Page - Compare forecasting models
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
from src.evaluation import evaluate_model, compare_models

st.set_page_config(page_title="Model Comparison", page_icon="🔍", layout="wide")

st.markdown("# 🔍 Model Comparison")
st.markdown("Compare performance of different forecasting models")


def run_model_comparison(df: pd.DataFrame, horizon: int = 7) -> dict:
    """Run all models and collect results"""
    results = {}
    
    # Get training and test data
    test_size = min(horizon, len(df) // 5)
    train_df = df.iloc[:-test_size]
    test_df = df.iloc[-test_size:]
    
    train_series = train_df.set_index('date')['close']
    actual = test_df['close'].values
    test_dates = test_df['date'].values
    
    # ARIMA
    try:
        from src.models.arima_model import ARIMAModel
        with st.spinner("Training ARIMA..."):
            model = ARIMAModel()
            model.fit(train_series, order=(2, 1, 2))
            forecast = model.predict(test_size)
            results['ARIMA'] = {
                'forecast': forecast, 'actual': actual, 'dates': test_dates,
                'metrics': evaluate_model(actual, forecast['forecast'].values, 'ARIMA')
            }
            st.success("✅ ARIMA complete")
    except Exception as e:
        st.warning(f"ARIMA failed: {str(e)[:50]}")
    
    # SARIMA
    try:
        from src.models.sarima_model import SARIMAModel
        with st.spinner("Training SARIMA..."):
            model = SARIMAModel(seasonal_period=7)
            model.fit(train_series, order=(1, 1, 1), seasonal_order=(1, 0, 1, 7))
            forecast = model.predict(test_size)
            results['SARIMA'] = {
                'forecast': forecast, 'actual': actual, 'dates': test_dates,
                'metrics': evaluate_model(actual, forecast['forecast'].values, 'SARIMA')
            }
            st.success("✅ SARIMA complete")
    except Exception as e:
        st.warning(f"SARIMA failed: {str(e)[:50]}")
    
    # Prophet
    try:
        from src.models.prophet_model import ProphetModel
        with st.spinner("Training Prophet..."):
            model = ProphetModel()
            model.fit(train_df, date_col='date', value_col='close')
            forecast = model.predict(test_size)
            results['Prophet'] = {
                'forecast': forecast, 'actual': actual, 'dates': test_dates,
                'metrics': evaluate_model(actual, forecast['forecast'].values, 'Prophet')
            }
            st.success("✅ Prophet complete")
    except Exception as e:
        st.warning(f"Prophet failed: {str(e)[:50]}")
    
    return results


def main():
    available_symbols = [s for s in get_available_symbols() if s in config.CRYPTO_LIST]
    
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        coin_id = st.selectbox("Select Coin", options=available_symbols,
            format_func=lambda x: f"{x} - {config.CRYPTO_LIST.get(x, {}).get('name', x)}")
    
    with col2:
        horizon = st.selectbox("Forecast Horizon", options=[7, 14, 30], index=0)
    
    # Load data
    try:
        with st.spinner(f"Loading {coin_id} data..."):
            df = load_coin_data(coin_id)
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return
    
    st.markdown("---")
    
    if st.button("🚀 Run Model Comparison", use_container_width=True, type="primary"):
        st.markdown("### Training Models...")
        results = run_model_comparison(df, horizon)
        
        if results:
            st.session_state['comparison_results'] = results
            st.session_state['comparison_coin'] = coin_id
    
    # Display results
    if 'comparison_results' in st.session_state and st.session_state.get('comparison_coin') == coin_id:
        results = st.session_state['comparison_results']
        
        st.markdown("---")
        st.markdown("### 📊 Model Performance Metrics")
        
        metrics_data = [r['metrics'] for r in results.values()]
        if metrics_data:
            comparison_df = compare_models(metrics_data)
            best_model = comparison_df.iloc[0]['model']
            
            st.success(f"🏆 **Best Model:** {best_model} (MAPE: {comparison_df.iloc[0]['mape']:.2f}%)")
            st.dataframe(comparison_df[['rank', 'model', 'mape', 'rmse', 'mae', 'r2']],
                use_container_width=True, hide_index=True)
        
        # Metrics Chart
        st.markdown("---")
        st.markdown("### 📈 Performance Comparison")
        
        models = list(results.keys())
        mapes = [results[m]['metrics']['mape'] for m in models]
        
        fig = go.Figure(data=[go.Bar(x=models, y=mapes, marker_color='#00D4FF',
            text=[f"{v:.2f}%" for v in mapes], textposition='outside')])
        fig.update_layout(title='MAPE Comparison (Lower is Better)',
            xaxis_title='Model', yaxis_title='MAPE (%)', template='plotly_dark', height=350)
        st.plotly_chart(fig, use_container_width=True)
        
        # Forecast Comparison
        st.markdown("### 🔮 Forecast Comparison")
        
        fig = go.Figure()
        colors = {'ARIMA': '#00D4FF', 'SARIMA': '#FFD700', 'Prophet': '#FF6B6B', 'LSTM': '#00FF88'}
        
        actual = list(results.values())[0]['actual']
        dates = list(results.values())[0]['dates']
        
        fig.add_trace(go.Scatter(x=dates, y=actual, mode='lines+markers', name='Actual',
            line=dict(color='white', width=3), marker=dict(size=8)))
        
        for model_name, result in results.items():
            fig.add_trace(go.Scatter(x=dates, y=result['forecast']['forecast'].values,
                mode='lines', name=model_name, line=dict(color=colors.get(model_name, '#888'), width=2)))
        
        fig.update_layout(title='Forecast vs Actual', xaxis_title='Date',
            yaxis_title='Price (USD)', template='plotly_dark', hovermode='x unified', height=400)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("👆 Click 'Run Model Comparison' to train and compare forecasting models.")


if __name__ == "__main__":
    main()
