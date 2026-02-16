# 📊 Cryptocurrency Time Series Analysis & Forecasting Dashboard

An interactive web dashboard for analyzing cryptocurrency prices using time series forecasting models including ARIMA, SARIMA, Prophet, and LSTM.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://pendyalapradeepreddy-cryptocurrency-time-se-dashboardapp-ut3phg.streamlit.app/)

## 🚀 Live Demo

Visit the live dashboard: **[Crypto Analytics Dashboard](https://pendyalapradeepreddy-cryptocurrency-time-se-dashboardapp-ut3phg.streamlit.app/)**


## 📈 Features

- **Multi-Coin Support**: Bitcoin (BTC), Ethereum (ETH), and 15 other cryptocurrencies
- **4 Forecasting Models**: ARIMA, SARIMA, Prophet, LSTM
- **Interactive Dashboard**: 7 pages with 10+ visualizations
- **Risk Analytics**: VaR, Sharpe ratio, Max Drawdown, Volatility regimes
- **Technical Indicators**: RSI, MACD, Bollinger Bands, Moving Averages

## 📁 Dashboard Pages

| Page | Description |
|------|-------------|
| 🏠 **Home** | Overview with KPIs, price charts, and technical indicators |
| 📊 **Executive Summary** | Market overview with sparklines and performance comparison |
| 📈 **Price Trends** | Detailed charts with candlesticks and indicators |
| 📊 **Volatility** | Risk metrics, VaR, drawdown analysis |
| 🔍 **Model Comparison** | Compare all 4 forecasting models side-by-side |
| 🔮 **Forecasts** | Generate price predictions with confidence intervals |
| ⚠️ **Risk Indicators** | Risk scores and automated market alerts |

## 🛠️ Tech Stack

- **Python 3.8+**
- **Streamlit** - Web dashboard framework
- **Plotly** - Interactive visualizations
- **Pandas & NumPy** - Data manipulation
- **Statsmodels & pmdarima** - ARIMA/SARIMA models
- **Prophet** - Facebook's time series library
- **TensorFlow/Keras** - LSTM neural network

## 📦 Installation

### Local Setup

1. Clone the repository:
```bash
git clone https://github.com/PendyalaPradeepReddy/Cryptocurrency-Time-Series-Analysis-.git
cd Cryptocurrency-Time-Series-Analysis-
```

2. Create a virtual environment:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# or
source venv/bin/activate  # Linux/Mac
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the dashboard:
```bash
streamlit run dashboard/app.py
```

The dashboard will open at `http://localhost:8501`

## 📊 Data Source

The project uses historical cryptocurrency data from **Kaggle** (3 years) stored in `main_df_enhanced.csv` with the following features:
- OHLC prices (Open, High, Low, Close)
- Volume and Market Cap
- Technical indicators (RSI, MACD, Bollinger Bands)
- Derived features (Returns, Volatility, Moving Averages)

**Dataset**: [Cryptocurrency Historical Data on Kaggle](https://www.kaggle.com)

## 🔮 Forecasting Models

### ARIMA
Auto-regressive Integrated Moving Average for linear trends and short-term forecasts.

### SARIMA  
Seasonal ARIMA with weekly patterns (period=7) for recurring market cycles.

### Prophet
Facebook's time series library handling seasonality and trend changes.

### LSTM
Deep learning neural network capturing complex nonlinear patterns.

## 📈 Key Metrics

- **MAPE**: Mean Absolute Percentage Error
- **RMSE**: Root Mean Squared Error
- **VaR**: Value at Risk (95%, 99%)
- **Sharpe Ratio**: Risk-adjusted returns
- **Max Drawdown**: Largest peak-to-trough decline

## 📝 Project Structure

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
│   ├── data_loader.py            # Data loading from CSV
│   ├── preprocessing.py          # Data cleaning
│   ├── eda.py                    # Visualizations
│   ├── evaluation.py             # Model metrics
│   ├── utils.py                  # Utility functions
│   └── models/
│       ├── arima_model.py
│       ├── sarima_model.py
│       ├── prophet_model.py
│       └── lstm_model.py
├── main_df_enhanced.csv          # Dataset
├── config.py                     # Configuration
├── requirements.txt              # Dependencies
└── README.md
```

## ⚠️ Disclaimer

This project is for **educational purposes only**. Cryptocurrency investments are highly volatile and risky. The forecasts provided should **not** be considered financial advice.

## 👨‍💻 Author

**Pradeep Reddy Pendyala**

- GitHub: [@PendyalaPradeepReddy](https://github.com/PendyalaPradeepReddy)

## 📄 License

MIT License - See LICENSE file for details

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Contact

For questions or feedback, please open an issue on GitHub.

---

**⭐ If you found this project helpful, please give it a star!**
