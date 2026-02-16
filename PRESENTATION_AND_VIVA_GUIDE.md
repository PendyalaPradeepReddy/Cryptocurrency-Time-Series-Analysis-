# 📊 Project Presentation & Viva Guide
## Cryptocurrency Time Series Analysis & Forecasting

---

# PART 1: HOW TO PRESENT THE PROJECT

---

## 🎯 Presentation Flow (Recommended 15–20 minutes)

### Slide 1: Title Slide (30 seconds)
> **"Cryptocurrency Time Series Analysis & Forecasting"**
> - Your Name, Roll Number, Department
> - Internship Organization Name
> - Mentor Name
> - Date

---

### Slide 2: Problem Statement (1–2 minutes)
> Say this:
> *"Cryptocurrency markets are extremely volatile and unpredictable. Investors and traders need data-driven tools to understand price trends, assess risk, and make informed decisions. My project builds a complete analytics system that collects real-time crypto data, performs analysis, and uses 4 different forecasting models to predict future prices — all presented through an interactive dashboard."*

**Key points to mention:**
- Crypto market is worth trillions of dollars but extremely volatile
- Traditional analysis methods are not enough
- Need for automated, data-driven forecasting tools
- This project addresses all three: **data collection → analysis → forecasting**

---

### Slide 3: Objectives (1 minute)
List these objectives:
1. Collect historical price data for 17 cryptocurrencies using CoinGecko API
2. Clean and preprocess the data (handle missing values, duplicates, ensure daily frequency)
3. Perform Exploratory Data Analysis (EDA) with 10+ interactive visualizations
4. Build and compare 4 time series forecasting models (ARIMA, SARIMA, Prophet, LSTM)
5. Calculate risk metrics (VaR, Sharpe Ratio, Max Drawdown, Volatility)
6. Build an interactive Streamlit dashboard with 6 pages for real-time analysis

---

### Slide 4: Tech Stack / Tools Used (1 minute)
| Category | Tools |
|----------|-------|
| Language | Python 3.x |
| Data Collection | CoinGecko REST API, Requests |
| Data Processing | Pandas, NumPy |
| Visualization | Plotly, Matplotlib, Seaborn |
| Statistical Models | Statsmodels, pmdarima (ARIMA, SARIMA) |
| ML Model | Facebook Prophet |
| Deep Learning | TensorFlow/Keras (LSTM) |
| Dashboard | Streamlit |
| Others | scikit-learn (MinMaxScaler) |

---

### Slide 5: System Architecture / Workflow (2 minutes)
> Draw or show this pipeline:

```
CoinGecko API → Data Collection → Raw Data (CSV)
                                       ↓
                              Data Preprocessing
                         (Missing values, Duplicates,
                          Derived Features, Technical Indicators)
                                       ↓
                              Processed Data (CSV)
                                       ↓
                    ┌──────────────┬──────────────┐
                    ↓              ↓              ↓
                   EDA        Forecasting     Risk Analysis
              (10+ Charts)   (4 Models)    (VaR, Sharpe, etc.)
                    ↓              ↓              ↓
                    └──────────────┴──────────────┘
                                       ↓
                         Streamlit Dashboard (6 Pages)
```

---

### Slide 6: Data Collection (1–2 minutes)
**Explain:**
- **Source**: CoinGecko API (free tier, no API key needed)
- **17 cryptocurrencies**: BTC, ETH, ADA, DOGE, XRP, DOT, LINK, LTC, UNI, BCH, ALGO, AAVE, EOS, ETC, FIL, GRT, XLM
- **~3 years of daily data** (1095 days)
- **Columns collected**: Date, Open, High, Low, Close, Volume, Market Cap
- **Rate limiting**: 1.5 second delay between API calls to avoid blocking
- Data saved in both raw and processed CSV formats

---

### Slide 7: Data Preprocessing (2 minutes)
**Explain the preprocessing pipeline:**

1. **Handle Missing Values** → Forward fill for prices, 0 for volume
2. **Remove Duplicates** → Based on date, keep latest
3. **Ensure Daily Frequency** → Fill gaps with forward-filled values
4. **Derived Features Created**:
   - **Returns**: Daily returns, Log returns
   - **Moving Averages**: SMA (7, 30, 90 day), EMA (7, 30 day)
   - **Volatility**: Rolling 7, 21, 30 day + Annualized
   - **Momentum**: 7-day and 30-day price momentum
   - **Technical Indicators**: RSI (14-day), MACD, Bollinger Bands
   - **Volume Features**: Volume SMA, Volume ratio

> *"After preprocessing, each coin's dataset has 30+ columns of features derived from just the basic price data."*

---

### Slide 8: Exploratory Data Analysis (2 minutes)
**Show screenshots/demo of these visualizations:**

1. 📈 **Price History Chart** — with 7-day and 30-day moving averages
2. 🕯️ **Candlestick Chart** — OHLC visualization
3. 📊 **Volume Chart** — colored by price movement (green/red)
4. 📉 **Volatility Chart** — rolling 21-day volatility over time
5. 📊 **Returns Distribution** — histogram with mean return line
6. 🔥 **Correlation Heatmap** — cross-crypto correlation matrix
7. 📏 **Bollinger Bands** — price with upper/lower bands
8. 📊 **RSI Chart** — with overbought (70) / oversold (30) lines
9. 📉 **MACD Chart** — MACD line, Signal line, Histogram
10. 🔄 **Multi-Coin Comparison** — normalized price comparison (base=100)

---

### Slide 9–12: Forecasting Models (4–5 minutes — spend most time here)

#### Model 1: ARIMA (Auto-Regressive Integrated Moving Average)
- **What it does**: Captures linear trends and short-term patterns
- **How**: Uses `pmdarima.auto_arima` for automatic (p, d, q) selection via AIC
- **Parameters**: max_p=5, max_d=2, max_q=5
- **Output**: Point forecast + 95% confidence intervals
- **Best for**: Short-term, linear trend forecasting

#### Model 2: SARIMA (Seasonal ARIMA)
- **What it does**: Extends ARIMA by adding weekly seasonality
- **How**: Uses SARIMAX from statsmodels with seasonal period = 7 (weekly)
- **Parameters**: Auto-selected (p,d,q)(P,D,Q,7)
- **Why**: Crypto markets show patterns based on weekdays (e.g., weekends have less trading)
- **Best for**: Capturing recurring weekly patterns

#### Model 3: Prophet (Facebook/Meta)
- **What it does**: Decomposes time series into trend + seasonality + holidays
- **How**: Additive model with Fourier terms for seasonality
- **Customization**: Added monthly seasonality (period=30.5, fourier_order=5)
- **Key parameter**: changepoint_prior_scale = 0.05 (controls trend flexibility)
- **Best for**: Handling trend changes and multiple seasonalities

#### Model 4: LSTM (Long Short-Term Memory Neural Network)
- **What it does**: Deep learning model that captures complex nonlinear patterns
- **Architecture**: 2 LSTM layers (50 units each) + Dropout (0.2) + Dense layers
- **Input**: Lookback window of 60 days
- **Training**: 50 epochs, batch size 32, Early Stopping (patience=10)
- **Scaling**: MinMaxScaler (0 to 1) for normalization
- **Best for**: Capturing complex, nonlinear dependencies

---

### Slide 13: Model Evaluation & Comparison (1–2 minutes)
**Metrics used:**

| Metric | What it Measures | Lower/Higher is Better |
|--------|------------------|----------------------|
| **MAPE** | Average % error | Lower ✅ |
| **RMSE** | Punishes large errors more | Lower ✅ |
| **MAE** | Average absolute error | Lower ✅ |
| **R²** | How well the model explains variance | Higher ✅ |

**Also performed:**
- Rolling Window Cross-Validation (window=100, horizon=7, step=30)
- Residual analysis (scatter plot + distribution)
- Visual forecast comparison chart

---

### Slide 14: Risk Analytics (1 minute)
- **Value at Risk (VaR)** at 95% and 99% — worst expected daily loss
- **Sharpe Ratio** — risk-adjusted returns (return per unit of risk)
- **Max Drawdown** — largest peak-to-trough decline
- **Annualized Volatility** — yearly risk measure
- **Volatility Regime Detection** — identify high/low risk periods

---

### Slide 15: Dashboard Demo (2 minutes)
> **Live demo the Streamlit dashboard** (`streamlit run dashboard/app.py`)

Show all 6 pages:
| # | Page | What to Show |
|---|------|--------------|
| 1 | **Home** | KPIs (price, volume, volatility, total return), price chart, technical indicators |
| 2 | **Executive Summary** | Market overview with sparklines |
| 3 | **Price Trends** | Detailed charts with SMA/EMA overlays |
| 4 | **Volatility** | Risk metrics, drawdown analysis |
| 5 | **Model Comparison** | Side-by-side model performance |
| 6 | **Forecasts** | Generate and view predictions |
| 7 | **Risk Indicators** | Risk scores and alerts |

---

### Slide 16: Results & Key Findings (1 minute)
> Mention observations like:
- "Prophet and LSTM generally performed better for longer-term forecasts"
- "ARIMA/SARIMA worked well for short-term (7-day) predictions"
- "High correlation observed between BTC and ETH returns"
- "Volatility tends to cluster — high volatility periods are followed by more high volatility"
- "The weekly seasonality captured by SARIMA improved predictions over basic ARIMA"

---

### Slide 17: Limitations & Future Scope (1 minute)

**Limitations:**
- CoinGecko free API has rate limits (limited to daily data)
- OHLC data is approximated (not accurate open/high/low)
- LSTM requires significant training time
- No sentiment analysis from social media/news

**Future Scope:**
- Add sentiment analysis (Twitter/Reddit data)
- Real-time streaming data pipeline
- Ensemble model combining all 4 models
- Portfolio optimization module
- Alert system for price anomalies
- Deploy dashboard to cloud (AWS/Heroku)

---

### Slide 18: Conclusion & Thank You (30 seconds)
> *"In this project, I built an end-to-end cryptocurrency analytics system that covers data collection, preprocessing, exploratory analysis, forecasting with 4 models, risk analytics, and an interactive dashboard. The system successfully demonstrates how data analytics can be applied to financial time series data for informed decision-making."*

---
---

# PART 2: EXPECTED VIVA QUESTIONS & ANSWERS

---

## 📌 Category 1: Project Overview Questions

---

### Q1: What is your project about? Explain in brief.
> **Answer:** My project is a **Cryptocurrency Time Series Analysis & Forecasting** system. It collects historical price data for 17 cryptocurrencies from the CoinGecko API, performs data cleaning and preprocessing, conducts exploratory data analysis with 10+ interactive visualizations, builds 4 forecasting models (ARIMA, SARIMA, Prophet, and LSTM), calculates risk metrics like VaR and Sharpe Ratio, and presents everything through a 6-page interactive Streamlit dashboard.

---

### Q2: Why did you choose this project/topic?
> **Answer:** Cryptocurrency markets are one of the most volatile financial markets. I wanted to apply data analytics and machine learning techniques to a real-world problem. This project allowed me to work with real API data, implement statistical and deep learning models, and build a full-stack analytics dashboard — covering the entire data analytics pipeline from collection to visualization.

---

### Q3: What problem does your project solve?
> **Answer:** Crypto investors and traders often make decisions based on gut feeling. My project provides a data-driven alternative by offering:
> - Historical price analysis and trend identification
> - Risk assessment through metrics like VaR and Sharpe Ratio
> - Price forecasting using 4 different models for comparison
> - An interactive dashboard for real-time exploration

---

### Q4: What is the dataset you used? How many records does it have?
> **Answer:** I used the CoinGecko API to collect approximately 3 years (~1095 days) of daily price data per cryptocurrency. I have 17 coins, so roughly 17 × 1095 = ~18,600 records. Each record includes date, open, high, low, close price, volume, and market cap. After preprocessing, each record is enriched with 30+ derived features like returns, moving averages, RSI, MACD, Bollinger Bands, and volatility measures.

---

### Q5: What are the columns/features in your dataset?
> **Answer:** The raw data has: **date, open, high, low, close, volume, market_cap**. After preprocessing, I add: **daily returns, log returns, SMA (7/30/90), EMA (7/30), volatility (7/21/30 day), annualized volatility, momentum (7/30 day), Bollinger Bands (upper/lower/middle/width), RSI, MACD (line/signal/histogram), volume SMA, volume ratio, and daily price range**.

---

## 📌 Category 2: Technical / Data Science Questions

---

### Q6: What is time series data? Why is it different from regular data?
> **Answer:** Time series data is a sequence of data points collected at successive time intervals. It's different from regular data because:
> 1. **Order matters** — you cannot shuffle rows randomly
> 2. **Temporal dependencies** — today's value depends on yesterday's value
> 3. **Seasonality** — patterns can repeat (weekly, monthly, yearly)
> 4. **Trend** — long-term increase or decrease
> 5. **Stationarity** — statistical properties may change over time
>
> In my project, the daily crypto prices form a time series.

---

### Q7: What is stationarity? Why is it important?
> **Answer:** A time series is **stationary** if its statistical properties (mean, variance, autocorrelation) remain constant over time. Most time series models like ARIMA require stationary data.
>
> Crypto prices are **non-stationary** (trending upward/downward), so I use **differencing** (the "I" in ARIMA, where d=1 or d=2) to make them stationary before modeling. The auto_arima function automatically selects the differencing order using statistical tests like ADF (Augmented Dickey-Fuller test).

---

### Q8: What is ARIMA? Explain (p, d, q).
> **Answer:** ARIMA stands for **Auto-Regressive Integrated Moving Average**:
> - **AR (p)**: The model uses `p` past values (lags) to predict the current value. Like saying "today's price depends on the last p days."
> - **I (d)**: The data is differenced `d` times to make it stationary. If d=1, we model the *change* in price instead of the actual price.
> - **MA (q)**: The model uses `q` past forecast errors to improve predictions.
>
> In my project, I use `pmdarima.auto_arima` to automatically find the best (p, d, q) by minimizing AIC (Akaike Information Criterion).

---

### Q9: What is SARIMA? How is it different from ARIMA?
> **Answer:** SARIMA is **Seasonal ARIMA**. It extends ARIMA by adding seasonal components:
> - ARIMA parameters: (p, d, q)
> - Seasonal parameters: (P, D, Q, m) where `m` is the seasonal period
>
> In my project, I set `m=7` (weekly seasonality) because crypto markets show weekly patterns (lower trading volume on weekends). SARIMA captures these recurring weekly patterns that regular ARIMA misses.

---

### Q10: What is Facebook Prophet? How does it work?
> **Answer:** Prophet is Meta/Facebook's open-source forecasting library. It decomposes a time series into:
> - **Trend**: Long-term growth or decline (using piecewise linear or logistic curves)
> - **Seasonality**: Recurring patterns modeled with Fourier series (weekly, yearly, custom)
> - **Holidays/Events**: Special days that affect the pattern
>
> The formula is: `y(t) = trend(t) + seasonality(t) + holidays(t) + error(t)`
>
> In my project, I enabled weekly and yearly seasonality, and added a custom monthly seasonality with fourier_order=5. The `changepoint_prior_scale=0.05` controls how flexible the trend is.

---

### Q11: What is LSTM? Why did you use it for time series?
> **Answer:** LSTM (Long Short-Term Memory) is a type of **Recurrent Neural Network (RNN)** designed to learn long-term dependencies. Regular RNNs suffer from the **vanishing gradient problem** — they forget earlier data. LSTM solves this with a **cell state** and three gates:
> - **Forget Gate**: Decides what to discard
> - **Input Gate**: Decides what new information to store
> - **Output Gate**: Decides what to output
>
> **My architecture:**
> - 2 LSTM layers with 50 units each
> - Dropout of 0.2 (to prevent overfitting)
> - Dense output layer
> - Input: 60-day lookback window → Predict next day's price
> - Trained with Adam optimizer, MSE loss
>
> I used LSTM because crypto prices have **complex, nonlinear patterns** that linear models (ARIMA) cannot capture.

---

### Q12: What evaluation metrics did you use? Explain each.
> **Answer:**
> - **MAPE (Mean Absolute Percentage Error)**: Average of absolute percentage errors. A MAPE of 5% means the model's predictions are off by 5% on average. Good for comparing across different price ranges.
> - **RMSE (Root Mean Squared Error)**: Square root of average squared errors. Penalizes large errors more heavily than small errors.
> - **MAE (Mean Absolute Error)**: Average of absolute errors in the same unit as the data (USD). Easy to interpret.
> - **R² (R-squared)**: Measures how much variance in the actual data is explained by the model. R²=1 is perfect, R²=0 means the model is no better than predicting the mean.

---

### Q13: What is RSI? How do you calculate it?
> **Answer:** RSI (Relative Strength Index) is a momentum indicator that measures the speed and magnitude of price changes. It ranges from 0 to 100.
> - **RSI > 70** → Overbought (price may drop)
> - **RSI < 30** → Oversold (price may rise)
>
> **Calculation (14-day period):**
> 1. Calculate daily price changes
> 2. Separate into gains (positive) and losses (negative)
> 3. Calculate 14-day rolling average of gains and losses
> 4. RS = Average Gain / Average Loss
> 5. RSI = 100 - (100 / (1 + RS))

---

### Q14: What are Bollinger Bands?
> **Answer:** Bollinger Bands are a volatility indicator with three lines:
> - **Middle Band**: 30-day Simple Moving Average (SMA)
> - **Upper Band**: SMA + 2 × Standard Deviation
> - **Lower Band**: SMA - 2 × Standard Deviation
>
> When price touches the **upper band**, it may be overbought. When it touches the **lower band**, it may be oversold. When the bands **squeeze** (get narrow), a big price move is expected.
>
> The **Bollinger Band Width** = (Upper - Lower) / Middle, which I calculate in preprocessing.

---

### Q15: What is MACD? How does it help in analysis?
> **Answer:** MACD (Moving Average Convergence Divergence) is a trend-following momentum indicator:
> - **MACD Line** = 12-day EMA − 26-day EMA
> - **Signal Line** = 9-day EMA of MACD Line
> - **Histogram** = MACD Line − Signal Line
>
> **Trading signals:**
> - When MACD crosses **above** Signal → Bullish (buy signal)
> - When MACD crosses **below** Signal → Bearish (sell signal)
> - Positive histogram = upward momentum

---

### Q16: What is Value at Risk (VaR)?
> **Answer:** VaR estimates the **maximum potential loss** over a given time period at a certain confidence level.
> - **VaR at 95%** means: "There is only a 5% chance that the daily loss will exceed this amount."
> - **VaR at 99%** means: "There is only a 1% chance that the daily loss will exceed this amount."
>
> For example, if Bitcoin's VaR(95%) = -3.5%, it means with 95% confidence, you won't lose more than 3.5% of your investment in a single day.

---

### Q17: What is the Sharpe Ratio?
> **Answer:** The Sharpe Ratio measures **risk-adjusted return** — how much return you get per unit of risk.
> - **Formula**: Sharpe Ratio = (Mean Return − Risk-Free Rate) / Standard Deviation of Returns
> - In my project, I annualize it: multiply by √365 (since crypto trades 365 days/year)
> - **Sharpe > 1**: Good risk-adjusted returns
> - **Sharpe < 0**: Returns are worse than a risk-free investment

---

### Q18: What is Max Drawdown?
> **Answer:** Max Drawdown is the **largest percentage decline** from a peak to a trough in the price. It measures the worst-case scenario for an investor.
> - **Formula**: Max Drawdown = (Trough Value − Peak Value) / Peak Value
> - For example, if Bitcoin's peak was $69,000 and it dropped to $16,000, the drawdown is (16000 - 69000) / 69000 = -76.8%

---

### Q19: Why did you use 4 models instead of just 1?
> **Answer:** Different models have different strengths:
> - **ARIMA**: Best for short-term, linear trends
> - **SARIMA**: Captures weekly seasonality that ARIMA misses
> - **Prophet**: Handles trend changes and multiple seasonalities easily
> - **LSTM**: Captures complex nonlinear patterns
>
> By comparing all 4, I can show which model works best for different scenarios and give the user a more reliable forecast. No single model is perfect for all situations — this is why **ensemble methods** are common in production systems.

---

### Q20: What is auto_arima? Why did you use it?
> **Answer:** `auto_arima` from the `pmdarima` library automatically searches for the best (p, d, q) combination by fitting multiple ARIMA models and selecting the one with the lowest **AIC (Akaike Information Criterion)**. AIC balances model fit and complexity — it penalizes overly complex models.
>
> I used it because manually testing all combinations of p, d, q is time-consuming and error-prone. `auto_arima` uses a **stepwise** algorithm for efficiency.

---

## 📌 Category 3: Implementation / Coding Questions

---

### Q21: What libraries/frameworks did you use?
> **Answer:**
> - `pandas`, `numpy` — Data manipulation
> - `requests` — API calls to CoinGecko
> - `statsmodels`, `pmdarima` — ARIMA/SARIMA models
> - `prophet` — Facebook Prophet model
> - `tensorflow.keras` — LSTM neural network
> - `scikit-learn` — MinMaxScaler for data normalization
> - `plotly` — Interactive charts
> - `matplotlib`, `seaborn` — Static visualizations
> - `streamlit` — Web dashboard

---

### Q22: How does your data preprocessing pipeline work?
> **Answer:** My `preprocess_data()` function runs 4 steps in sequence:
> 1. `handle_missing_values()` — Forward-fills prices, fills volume with 0
> 2. `remove_duplicates()` — Removes duplicate dates, keeps the latest entry
> 3. `ensure_daily_frequency()` — Creates complete date range, fills gaps with forward-fill
> 4. `add_derived_features()` — Calculates 25+ technical indicators and features
>
> This ensures clean, consistent, feature-rich data for modeling.

---

### Q23: How did you handle missing values?
> **Answer:** For **price columns** (open, high, low, close), I used **forward fill** (`ffill`) — meaning if a day's price is missing, I use the previous day's price. This is appropriate for financial data because the last known price is the best estimate.
>
> For **volume** and **market cap**, I filled missing values with **0**, since missing volume likely means no trading happened.

---

### Q24: How does the LSTM input work? What is the lookback window?
> **Answer:** The lookback window (60 days) defines how many past days the LSTM looks at to predict the next day.
> - I take the last 60 days of closing prices
> - Normalize them using MinMaxScaler (scale to 0–1 range)
> - Create sliding window sequences: [Day1–Day60] → predict Day61, [Day2–Day61] → predict Day62, etc.
> - Reshape to 3D array: [samples, timesteps(60), features(1)]
> - The LSTM learns patterns in these 60-day windows

---

### Q25: What is the architecture of your LSTM model?
> **Answer:**
> ```
> Input (60 timesteps × 1 feature)
>     ↓
> LSTM Layer 1 (50 units, return_sequences=True)
>     ↓
> Dropout (20%)
>     ↓
> LSTM Layer 2 (50 units, return_sequences=False)
>     ↓
> Dropout (20%)
>     ↓
> Dense Layer (25 neurons)
>     ↓
> Dense Layer (1 neuron — output)
> ```
> Compiled with **Adam optimizer** and **MSE loss**. Uses **EarlyStopping** with patience=10 to prevent overfitting.

---

### Q26: Why did you use Dropout in LSTM?
> **Answer:** Dropout randomly deactivates 20% of neurons during training. This prevents **overfitting** — where the model memorizes the training data instead of learning general patterns. This is especially important for financial data which is noisy and irregular.

---

### Q27: Why did you use MinMaxScaler for LSTM?
> **Answer:** LSTM networks work better with **normalized data** (values between 0 and 1) because:
> - Neural networks use gradient-based optimization, and large values can cause **exploding gradients**
> - It ensures all features are on the same scale
> - Sigmoid and tanh activation functions in LSTM work in the 0–1 and -1–1 range
> I use `MinMaxScaler(feature_range=(0, 1))` and then **inverse_transform** the predictions back to original scale.

---

### Q28: How does your Streamlit dashboard work?
> **Answer:** The dashboard is built with Streamlit and has:
> - **Main page** (`app.py`): Loads data, shows KPIs and charts
> - **6 sub-pages** in the `pages/` folder: Each handles a specific analysis area
> - **Session state**: Caches loaded data to avoid reloading on every interaction
> - **Sidebar controls**: Dropdown to select cryptocurrency, reload button
> - **Custom CSS**: Dark theme with gradient styling for premium look
> - **Plotly charts**: Interactive, zoomable, hoverable visualizations

---

### Q29: How does the CoinGecko API work? Are there any limitations?
> **Answer:** CoinGecko provides a **free REST API** for crypto market data:
> - Endpoint: `https://api.coingecko.com/api/v3/coins/{id}/market_chart`
> - Parameters: `vs_currency=usd`, `days=1095`, `interval=daily`
> - Returns JSON with prices, volumes, and market caps as timestamp–value pairs
>
> **Limitations:**
> - Free tier has rate limits (~10-30 calls/minute)
> - I added 1.5 second delay between calls
> - Only provides close price for daily data (not true OHLC)
> - I approximated High as close×1.02 and Low as close×0.98

---

### Q30: What is a confidence interval in your forecasts?
> **Answer:** A confidence interval gives a range where the actual price is likely to fall.
> - For ARIMA/SARIMA: I use 95% confidence intervals from the model's `get_forecast()` method, calculated using the model's standard error
> - For Prophet: Prophet directly provides `yhat_lower` and `yhat_upper`
> - For LSTM: I approximate using ±1.96 × (10% of historical standard deviation)
>
> A wider confidence interval means more uncertainty in the forecast.

---

## 📌 Category 4: Results & Analysis Questions

---

### Q31: Which model performed best?
> **Answer:** It depends on the cryptocurrency and forecast horizon:
> - For **short-term (7-day)** forecasts: **ARIMA/SARIMA** often perform well due to their ability to capture recent trends
> - For **medium-term (30-day)** forecasts: **Prophet** tends to be more robust because it handles trend changes well
> - **LSTM** can capture complex patterns but requires more data and tuning
> - I compare models using MAPE — the one with the **lowest MAPE** is ranked best

---

### Q32: What key insights did you find from EDA?
> **Answer:**
> 1. **High correlation** between Bitcoin and other altcoins — BTC tends to lead the market
> 2. **Volatility clustering** — periods of high volatility are followed by more high volatility
> 3. **Returns are not normally distributed** — they have fat tails (extreme events happen more than expected)
> 4. **Weekly patterns exist** — less trading activity on weekends
> 5. **RSI extremes often precede reversals** — useful for risk management

---

### Q33: What is the practical use of your project?
> **Answer:**
> - **For traders**: Can use technical indicators (RSI, MACD, Bollinger Bands) for buy/sell decisions
> - **For investors**: Can assess risk using VaR, Sharpe Ratio, and Max Drawdown before investing
> - **For analysts**: Can use the forecasting models to estimate future prices and compare model accuracy
> - **For students/researchers**: Can serve as a template for any time series analysis project

---

## 📌 Category 5: General Data Analytics Questions

---

### Q34: What is EDA? Why is it important?
> **Answer:** EDA (Exploratory Data Analysis) is the initial investigation of data to discover patterns, spot anomalies, check assumptions, and summarize data using statistics and visualizations. It is important because:
> - Helps understand the data before modeling
> - Identifies outliers and data quality issues
> - Reveals relationships between features
> - Guides feature engineering and model selection

---

### Q35: Difference between SMA and EMA?
> **Answer:**
> - **SMA (Simple Moving Average)**: Equal weight to all values in the window. SMA_7 = average of last 7 days.
> - **EMA (Exponential Moving Average)**: Gives more weight to recent values. More responsive to recent price changes.
> - EMA reacts faster to price changes, while SMA is smoother.
> - In my project, I calculate both SMA (7/30/90 day) and EMA (7/30 day).

---

### Q36: What is overfitting? How did you prevent it?
> **Answer:** Overfitting happens when a model learns the training data *too well*, including its noise, and fails on new data.
> **Prevention in my project:**
> - **ARIMA/SARIMA**: AIC-based model selection penalizes overly complex models
> - **Prophet**: `changepoint_prior_scale=0.05` regularizes trend flexibility
> - **LSTM**: Dropout (20%), EarlyStopping (patience=10), validation split (10%)
> - **Cross-Validation**: Rolling window CV to test on multiple time periods

---

### Q37: What is AIC? Why is it used for ARIMA?
> **Answer:** AIC (Akaike Information Criterion) is a metric that balances model **goodness of fit** with **complexity**.
> - AIC = 2k − 2ln(L), where k = number of parameters, L = likelihood
> - Lower AIC = better model
> - It prevents choosing an overly complex model that overfits
> - `auto_arima` tests many (p,d,q) combinations and picks the one with the lowest AIC

---

### Q38: What is the difference between a statistical model and a machine learning model?
> **Answer:**
> | Statistical Model (ARIMA, SARIMA) | ML Model (Prophet, LSTM) |
> |---|---|
> | Based on mathematical equations | Learns patterns from data |
> | Requires stationarity assumptions | More flexible, fewer assumptions |
> | Interpretable parameters | Can be black-box (LSTM) |
> | Better for linear patterns | Better for complex/nonlinear patterns |
> | Lighter, faster to train | May need more data and computation |
>
> My project uses both to compare their strengths.

---

### Q39: Can your model predict market crashes?
> **Answer:** Not directly. **No model can reliably predict sudden market crashes** because crashes are often caused by unforeseen events (regulations, hacks, macroeconomic shocks). However:
> - **Volatility indicators** can show increasing risk
> - **Max Drawdown** measures historical worst-case scenarios
> - **VaR** gives expected loss limits
> - **Widening Bollinger Bands** and extreme RSI can signal instability
>
> My project is best used for **risk awareness**, not guaranteed crash prediction.

---

### Q40: If you had more time, what would you improve?
> **Answer:**
> 1. **Sentiment Analysis**: Integrate Twitter/Reddit sentiment using NLP
> 2. **Ensemble Model**: Combine all 4 model predictions with weighted averaging
> 3. **Real-time Dashboard**: Use WebSocket for live price streaming
> 4. **More Coins**: Expand to 50+ cryptocurrencies
> 5. **Cloud Deployment**: Host on AWS/Heroku for public access
> 6. **Alert System**: Email/SMS notifications for price anomalies
> 7. **Portfolio Optimization**: Modern Portfolio Theory (MPT) with Markowitz frontier
> 8. **More Advanced Models**: Transformer-based models (like TFT — Temporal Fusion Transformer)

---

## 📌 Quick Revision Cheat Sheet

| Topic | One-Liner to Remember |
|-------|----------------------|
| ARIMA | Auto-regressive + differencing + moving average for linear trends |
| SARIMA | ARIMA + weekly seasonality (m=7) |
| Prophet | Facebook's decomposition: trend + seasonality |
| LSTM | Neural network with memory gates for nonlinear patterns |
| RSI | Momentum: >70 overbought, <30 oversold |
| MACD | 12-day EMA minus 26-day EMA, with signal line |
| Bollinger Bands | SMA ± 2×std; squeeze = incoming big move |
| VaR | Max expected loss at 95%/99% confidence |
| Sharpe Ratio | Return per unit of risk |
| Max Drawdown | Biggest peak-to-trough drop |
| MAPE | Average percentage error |
| Stationarity | Constant mean and variance over time |
| AIC | Model selection: lower = better |
| Overfitting | Model memorizes noise; prevent with dropout/AIC/early stopping |

---

> 💡 **Final Tip**: During viva, always start with a **simple answer** and then add **technical depth**. If the mentor asks a follow-up, go deeper. Don't overwhelm them with jargon in the first sentence!

> **Good luck, Pradeep! You've got this! 🚀**
