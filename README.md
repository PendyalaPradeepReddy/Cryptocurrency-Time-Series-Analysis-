# 📊 Cryptocurrency Time Series Analysis & Forecasting

A comprehensive data analytics system for analyzing and forecasting cryptocurrency prices using multiple time series models with an interactive Streamlit dashboard.

## 🚀 Features

- **Multi-Coin Support**: Bitcoin (BTC), Ethereum (ETH), Solana (SOL)
- **4 Forecasting Models**: ARIMA, SARIMA, Prophet, LSTM
- **Interactive Dashboard**: 6 pages with 10+ visualizations
- **Risk Analytics**: VaR, Sharpe ratio, max drawdown, volatility regimes
- **Technical Indicators**: RSI, MACD, Bollinger Bands, moving averages

## 📁 Project Structure

```
DA Project/
├── dashboard/
│   ├── app.py                    # Main dashboard
│   └── pages/
│       ├── 1_executive_summary.py
│       ├── 2_price_trends.py
│       ├── 3_volatility.py
│       ├── 4_model_comparison.py
│       ├── 5_forecasts.py
│       └── 6_risk_indicators.py
├── src/
│   ├── data_collection.py        # CoinGecko API
│   ├── preprocessing.py          # Data cleaning
│   ├── eda.py                    # Visualizations
│   ├── evaluation.py             # Model metrics
│   └── models/
│       ├── arima_model.py
│       ├── sarima_model.py
│       ├── prophet_model.py
│       └── lstm_model.py
├── data/
│   ├── raw/                      # Raw API data
│   └── processed/                # Cleaned data
├── models/saved/                 # Trained models
├── config.py                     # Configuration
├── requirements.txt              # Dependencies
└── README.md
```

## 🛠️ Installation

1. **Create virtual environment** (recommended):
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # or
   source venv/bin/activate  # Linux/Mac
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the dashboard**:
   ```bash
   streamlit run dashboard/app.py
   ```

## 📊 Dashboard Pages

| Page | Description |
|------|-------------|
| **Home** | Main overview with KPIs and price charts |
| **Executive Summary** | Market overview with sparklines |
| **Price Trends** | Detailed charts with technical indicators |
| **Volatility** | Risk metrics, VaR, drawdown analysis |
| **Model Comparison** | Compare all 4 forecasting models |
| **Forecasts** | Generate and visualize predictions |
| **Risk Indicators** | Risk scores and market alerts |

## 🔮 Forecasting Models

### ARIMA
- Auto-regressive Integrated Moving Average
- Best for linear trends and short-term forecasts

### SARIMA
- Seasonal ARIMA with weekly patterns
- Captures recurring patterns in crypto markets

### Prophet
- Facebook's time series library
- Handles seasonality and trend changes

### LSTM
- Deep learning neural network
- Captures complex nonlinear patterns

## 📈 Key Metrics

- **MAPE**: Mean Absolute Percentage Error
- **RMSE**: Root Mean Squared Error
- **VaR**: Value at Risk (95%, 99%)
- **Sharpe Ratio**: Risk-adjusted returns
- **Max Drawdown**: Largest peak-to-trough decline

## ⚙️ Configuration

Edit `config.py` to customize:
- API settings
- Supported cryptocurrencies
- Model hyperparameters
- Dashboard theme

## 🔒 Data Sources

- **CoinGecko API** (Free tier)
- Rate limited to prevent blocks
- ~3 years of historical data

## ⚠️ Disclaimer

This project is for **educational purposes only**. Cryptocurrency investments are highly volatile and risky. The forecasts provided should not be considered financial advice.

## 📝 License

MIT License

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
