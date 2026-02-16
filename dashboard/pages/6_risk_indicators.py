"""
Risk Indicators Page - Advanced risk metrics and alerts
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

st.set_page_config(page_title="Risk Indicators", page_icon="⚠️", layout="wide")

st.markdown("# ⚠️ Risk Indicators")
st.markdown("Advanced risk metrics and market condition alerts")


def calculate_risk_score(df: pd.DataFrame) -> dict:
    """Calculate overall risk score"""
    returns = df['close'].pct_change().dropna()
    
    vol_score = min(returns.std() * np.sqrt(365) * 100, 100)
    dd = abs(calculate_max_drawdown(df['close']))
    dd_score = min(dd * 200, 100)
    var = abs(np.percentile(returns, 5))
    var_score = min(var * 1000, 100)
    
    overall = (vol_score * 0.4 + dd_score * 0.4 + var_score * 0.2)
    
    return {'overall': overall, 'volatility': vol_score, 'drawdown': dd_score, 'var': var_score}


def get_risk_level(score: float) -> tuple:
    """Get risk level label and color"""
    if score < 30: return "LOW", "#00FF88"
    elif score < 50: return "MODERATE", "#FFD700"
    elif score < 70: return "HIGH", "#FF8C00"
    else: return "EXTREME", "#FF4444"


def main():
    available_symbols = [s for s in get_available_symbols() if s in config.CRYPTO_LIST]
    
    coin_id = st.selectbox("Select Coin", options=available_symbols,
        format_func=lambda x: f"{x} - {config.CRYPTO_LIST.get(x, {}).get('name', x)}")
    
    # Load data
    try:
        with st.spinner(f"Loading {coin_id} data..."):
            df = load_coin_data(coin_id)
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return
    
    coin_name = config.CRYPTO_LIST.get(coin_id, {}).get('name', coin_id)
    
    # Calculate risk scores
    risk_scores = calculate_risk_score(df)
    overall_level, overall_color = get_risk_level(risk_scores['overall'])
    
    st.markdown("---")
    
    # Risk Gauge and Breakdown
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### Overall Risk Level")
        
        fig = go.Figure(go.Indicator(
            mode="gauge+number", value=risk_scores['overall'],
            domain={'x': [0, 1], 'y': [0, 1]}, title={'text': f"{coin_id} Risk Score"},
            gauge={
                'axis': {'range': [0, 100]}, 'bar': {'color': overall_color},
                'steps': [
                    {'range': [0, 30], 'color': 'rgba(0, 255, 136, 0.3)'},
                    {'range': [30, 50], 'color': 'rgba(255, 215, 0, 0.3)'},
                    {'range': [50, 70], 'color': 'rgba(255, 140, 0, 0.3)'},
                    {'range': [70, 100], 'color': 'rgba(255, 68, 68, 0.3)'}
                ]
            }
        ))
        fig.update_layout(template='plotly_dark', height=250, margin=dict(l=20, r=20, t=50, b=20))
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown(f"""
        <div style="text-align: center; padding: 10px; background: {overall_color}22; 
        border-radius: 10px; border: 2px solid {overall_color};">
            <h2 style="color: {overall_color}; margin: 0;">{overall_level} RISK</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### Risk Factor Breakdown")
        
        factors = [
            ('Volatility', risk_scores['volatility'], 'Price fluctuation intensity'),
            ('Drawdown', risk_scores['drawdown'], 'Peak-to-trough decline'),
            ('Value at Risk', risk_scores['var'], 'Daily loss potential')
        ]
        
        for name, score, desc in factors:
            level, color = get_risk_level(score)
            st.markdown(f"**{name}** ({level})")
            st.progress(score / 100)
            st.caption(f"{desc}: {score:.1f}/100")
    
    # Risk Alerts
    st.markdown("---")
    st.markdown("### 🚨 Risk Alerts")
    
    returns = df['close'].pct_change().dropna()
    vol_ann = returns.std() * np.sqrt(365) * 100
    
    alerts = []
    if vol_ann > 100:
        alerts.append(("error", f"⚠️ **Extreme Volatility** - {vol_ann:.1f}% annualized"))
    elif vol_ann > 70:
        alerts.append(("warning", f"⚡ **High Volatility** - {vol_ann:.1f}% annualized"))
    
    momentum = (df['close'].iloc[-1] / df['close'].iloc[0] - 1) * 100
    if momentum < -20:
        alerts.append(("error", f"📉 **Sharp Decline** - Price down {abs(momentum):.1f}%"))
    
    if 'rsi' in df.columns:
        rsi = df['rsi'].iloc[-1]
        if rsi > 70:
            alerts.append(("warning", f"🔴 **Overbought** - RSI at {rsi:.1f}"))
        elif rsi < 30:
            alerts.append(("info", f"🟢 **Oversold** - RSI at {rsi:.1f}"))
    
    if not alerts:
        st.success("✅ No significant risk alerts")
    else:
        for alert_type, message in alerts:
            if alert_type == "error": st.error(message)
            elif alert_type == "warning": st.warning(message)
            else: st.info(message)
    
    # Historical Risk Chart
    st.markdown("---")
    st.markdown("### 📊 Historical Risk Analysis")
    
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.1,
        row_heights=[0.5, 0.5], subplot_titles=('Price', 'Rolling Volatility & Drawdown'))
    
    fig.add_trace(go.Scatter(x=df['date'], y=df['close'], line=dict(color='#00D4FF', width=2),
        name='Price'), row=1, col=1)
    
    rolling_vol = returns.rolling(21).std() * np.sqrt(365) * 100
    fig.add_trace(go.Scatter(x=df['date'], y=rolling_vol, line=dict(color='#FF6B6B', width=1),
        name='Volatility'), row=2, col=1)
    
    peak = df['close'].expanding().max()
    drawdown = ((df['close'] - peak) / peak) * 100
    fig.add_trace(go.Scatter(x=df['date'], y=drawdown, line=dict(color='#FFD700', width=1),
        name='Drawdown'), row=2, col=1)
    
    fig.update_layout(template='plotly_dark', height=500, showlegend=True, hovermode='x unified')
    st.plotly_chart(fig, use_container_width=True)


if __name__ == "__main__":
    main()
