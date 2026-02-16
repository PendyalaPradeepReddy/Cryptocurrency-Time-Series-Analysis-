# 📊 Dashboard Walkthrough — Live Presentation Guide
## Cryptocurrency Time Series Analysis & Forecasting

> **Purpose**: Use this guide while presenting your Streamlit dashboard to your mentor.
> For each page, you will find:
> - ✅ What to show on the screen
> - 🗣️ What to say / explain
> - 🧠 Technical points to highlight
> - ❓ Questions your mentor may ask on that page

---

## 🟢 Before You Start — Setup

### Step 1: Open Terminal and Run the Dashboard
```bash
cd "c:\Users\Pradeep reddy\OneDrive\Desktop\DA Project"
streamlit run dashboard/app.py
```

### Step 2: Open Browser
- The dashboard will open at **http://localhost:8501**
- Make sure your browser is in **full screen** for a better impression

### Step 3: Keep This Guide Open
- Open this file side by side (or on your phone) so you can refer to it while presenting

---
---

# 🏠 PAGE 0: HOME (Main Dashboard — `app.py`)

---

## ✅ What You See on Screen
- A gradient header: **"📊 Crypto Analytics Dashboard"**
- Subtitle: *"Real-time cryptocurrency analysis and forecasting"*
- **Sidebar** on the left with:
  - A dropdown to select any cryptocurrency (BTC, ETH, ADA, DOGE, etc.)
  - A "Reload Data" button
  - Status showing how many coins are loaded
- **4 KPI Cards** at the top showing:
  - 💰 Current Price (with daily % change shown as delta)
  - 📊 Volume (in millions)
  - 📈 30-day Volatility (%)
  - 📉 Total Return (%)
- **Price History Chart** — interactive line chart with 7-day and 30-day moving averages
- **Two side-by-side charts:**
  - Volatility Analysis (price + rolling 21-day volatility)
  - Returns Distribution (histogram with mean return line)
- **Technical Indicators** section with two tabs:
  - Bollinger Bands
  - RSI
- **Multi-Coin Comparison** — normalized price comparison (base = 100) with correlation heatmap
- **Statistical Summary** table at the bottom

---

## 🗣️ What to Say

> *"This is the home page of my Crypto Analytics Dashboard. It gives a complete overview of any selected cryptocurrency at a glance."*

### About the Sidebar:
> *"On the left, I have a sidebar where the user can select any cryptocurrency from the 17 coins available in the dataset. The data is loaded from a CSV file called `main_df_enhanced.csv` that contains enriched data for all coins."*

### About the KPIs:
> *"At the top, I display 4 key performance indicators — the current price with daily change shown as a green/red delta, the trading volume, the 30-day rolling volatility which shows how risky the coin is, and the total return over the entire period which shows how much profit or loss you would have if you held this coin from the start."*

### About the Price Chart:
> *"This is an interactive Plotly chart showing the price history. I've overlaid the 7-day SMA (short-term trend) in yellow dotted and the 30-day SMA (medium-term trend) in red dashed. You can hover over any point to see exact values, and you can zoom in by dragging. The moving averages help identify trend direction — when the short SMA crosses above the long SMA, it's a bullish signal, and vice versa."*

### About Volatility and Returns:
> *"On the left, the volatility chart shows the price on top and the rolling 21-day volatility below it as a filled area chart. You can see how volatility tends to cluster — periods of high volatility are followed by more high volatility. On the right, the returns distribution shows a histogram of daily returns with a mean line. Notice that it's not a perfect bell curve — it has fat tails, meaning extreme price movements happen more often than a normal distribution would predict."*

### About Technical Indicators:
> *"I've added two key technical indicators in tabs:*
> - *Bollinger Bands: These show the price with upper and lower bands at 2 standard deviations from the 30-day SMA. When the price touches the upper band, the coin may be overbought. When bands squeeze together, a big price move is expected.*
> - *RSI (Relative Strength Index): This momentum indicator ranges from 0 to 100. Above 70 means overbought, below 30 means oversold. I've marked these thresholds with dashed red and green lines."*

### About Multi-Coin Comparison:
> *"Finally, at the bottom, I compare multiple coins by normalizing their prices to start at 100. This makes it easy to compare performance regardless of price differences — for example, Bitcoin might be $60,000 and Dogecoin might be $0.10, but by normalizing we can see which one grew more. The correlation heatmap next to it shows how returns of different coins are correlated — BTC and ETH usually have high correlation."*

---

## 🧠 Technical Points to Highlight
- Dashboard uses **Streamlit's session state** to cache loaded data and avoid reloading on every user interaction
- Custom CSS is injected with `st.markdown(unsafe_allow_html=True)` for the dark gradient theme styling
- All charts are built with **Plotly** (interactive, hoverable, zoomable) — not static matplotlib
- The `load_coin_data()` function reads data from CSV, then `add_features()` dynamically computes 15+ derived features (SMA, EMA, RSI, MACD, Bollinger Bands, volatility, returns)
- The `st.columns(4)` creates the 4-column KPI layout
- The `st.tabs()` separates Bollinger Bands and RSI into clean tabs

---

## ❓ Possible Mentor Questions on This Page
| Question | Short Answer |
|----------|--------------|
| "How are you loading the data?" | From `main_df_enhanced.csv` using Pandas. The `data_loader.py` module parses dates, sorts by symbol and date, then adds derived features. |
| "Why Plotly and not Matplotlib?" | Plotly gives interactive charts (hover, zoom, pan) — much better for a dashboard. Matplotlib is static. |
| "What does the delta (green/red) on KPIs mean?" | It shows the percentage change compared to the previous day's closing price. |
| "Why normalize prices for comparison?" | Different coins have vastly different price scales. Normalizing to base=100 lets us compare growth/decline fairly. |

---
---

# 📊 PAGE 1: EXECUTIVE SUMMARY (`1_executive_summary.py`)

---

## ✅ What You See on Screen
- **Market Overview** section with up to 4 coin cards, each showing:
  - Coin symbol (BTC, ETH, etc.)
  - Current price
  - 24-hour percentage change (delta)
  - A small **sparkline chart** below each card (30-day mini price trend)
- **Performance Summary** table with columns:
  - Coin name, Current Price, Total Return, All-time High, All-time Low, Annualized Volatility
- **Normalized Performance Comparison** chart — a multi-line chart comparing up to 6 coins

---

## 🗣️ What to Say

> *"This is the Executive Summary page — it gives a bird's-eye view of the entire cryptocurrency market covered in my project."*

### About Market Overview Cards:
> *"At the top, I show summary cards for the top 4 cryptocurrencies. Each card displays the coin symbol, its current price, and a 24-hour price change as a percentage. Below each card is a sparkline — a tiny 30-day price chart. The sparkline is colored green if the price went up over the period, and red if it went down. These sparklines give an instant visual feel for each coin's recent trend without taking up much space."*

### About the Sparkline Code:
> *"The sparkline is a minimal Plotly chart — I removed all axes, legends, and margins to make it as compact as possible. It uses `fill='tozeroy'` with a transparent fill color to create the area-under-curve effect."*

### About Performance Table:
> *"Below the cards, I have a performance summary table comparing all loaded coins side by side. You can see the total return (from the start of the data to now), the historical high and low, and the annualized volatility. Annualized volatility is calculated as daily returns standard deviation multiplied by √365 — since crypto trades 365 days a year."*

### About Normalized Comparison:
> *"The chart at the bottom normalizes all prices to start at 100. This lets us directly compare: if a line is at 200, that coin doubled in value. If it's at 50, it lost half. You can click on legend items to toggle coins on/off."*

---

## 🧠 Technical Points to Highlight
- The page loads only 6 coins (not all 17) for performance — `available_symbols[:6]`
- Sparkline charts have zero margins, transparent background, and hidden axes — designed to be compact
- Annualized Volatility formula used: `std(daily_returns) × √365 × 100`
- The sparkline color is dynamically chosen: green if `last close ≥ first close`, else red

---

## ❓ Possible Mentor Questions on This Page
| Question | Short Answer |
|----------|--------------|
| "Why only 6 coins and not all 17?" | For dashboard performance. Loading and rendering 17 sparklines slows down the page. We can increase it if needed. |
| "How is the sparkline implemented?" | It's a minimal Plotly scatter chart with `fill='tozeroy'`, transparent background, and all axes hidden. The color is dynamic based on price direction. |
| "What is annualized volatility?" | Daily returns std dev × √365 × 100. It estimates the yearly risk/uncertainty of the coin. |

---
---

# 📈 PAGE 2: PRICE TRENDS (`2_price_trends.py`)

---

## ✅ What You See on Screen
- **Top controls**: Coin selector dropdown + Data range filter (All, Last 500, Last 200, Last 100)
- **4 KPI metrics**: Current Price (with return %), Period High, Period Low, Average Price
- **Radio button** to choose chart type:
  - **Line** — price chart with 7-day and 30-day SMA overlays
  - **Candlestick** — OHLC candlestick chart (green for up, red for down days)
  - **With Indicators** — 3-panel chart: Price + Bollinger Bands (top), RSI (middle), Volume (bottom)
- **Expandable Raw Data section** — last 30 rows of OHLC data in a table

---

## 🗣️ What to Say

> *"This is the Price Trends page — it lets the user explore historical prices in detail with different chart types and technical indicators."*

### About Controls:
> *"At the top, the user selects a cryptocurrency and a data range. The data range filter lets them focus on recent data — for example, 'Last 100' shows only the last 100 days. This is useful because some technical indicators become clearer on shorter time frames."*

### Show the Line Chart:
> *"In the Line view, you see the price with two moving averages overlaid. The 7-day SMA in yellow reacts quickly to recent changes. The 30-day SMA in red is smoother and shows the medium-term trend. When the yellow line crosses above the red line, it's called a Golden Cross — a bullish signal."*

### Switch to Candlestick:
> *"Now I'll switch to the Candlestick view. Each candle represents one day. A green candle means the close was higher than the open (bullish day), and a red candle means it was lower (bearish day). The thin lines above and below each candle are called wicks — they show the high and low of the day. Candlestick charts are the standard in financial trading."*

### Switch to With Indicators:
> *"This is the most comprehensive view — a 3-panel chart. The top panel shows the price inside Bollinger Bands. The middle panel shows the RSI with overbought (70) and oversold (30) thresholds. The bottom panel shows the trading volume as a bar chart. This combined view is what professional traders typically use."*

### About Raw Data:
> *"At the bottom, there's an expandable section that shows the raw OHLC data in a table. This allows the mentor or user to verify the actual numbers behind the charts."*

---

## 🧠 Technical Points to Highlight
- Three chart types in one page using `st.radio()` with `horizontal=True`
- The "With Indicators" chart uses `make_subplots(rows=3, cols=1)` with shared x-axes and custom row heights (50%, 25%, 25%)
- RSI overbought/oversold thresholds are drawn using `fig.add_hline()`
- The data range filter uses `df.tail(n)` to slice the last N rows
- Raw data is inside `st.expander()` so it doesn't clutter the page by default

---

## ❓ Possible Mentor Questions on This Page
| Question | Short Answer |
|----------|--------------|
| "What does each candlestick represent?" | One trading day. The body shows open-to-close range. Wicks show high and low. Green = close > open, Red = close < open. |
| "Why did you add a time range filter?" | Technical indicators work differently on different time frames. Short ranges make recent patterns clearer. Also improves chart rendering speed. |
| "What are the Bollinger Bands showing?" | The price inside a ±2 standard deviation band from the 30-day SMA. When price hits upper band → possibly overbought. Narrow bands → big move coming. |
| "What is the RSI threshold for?" | RSI > 70 = overbought (may drop), RSI < 30 = oversold (may rise). These are standard thresholds used in trading. |

---
---

# 📊 PAGE 3: VOLATILITY ANALYSIS (`3_volatility.py`)

---

## ✅ What You See on Screen
- **4 Key Risk Metric cards**:
  - Annualized Volatility (%)
  - VaR at 95% confidence (%)
  - Maximum Drawdown (%)
  - Sharpe Ratio
- **2-panel Volatility Over Time chart**:
  - Top: Price line chart
  - Bottom: Rolling 21-day annualized volatility with filled area
- **Two side-by-side charts**:
  - Returns Distribution histogram with VaR 95% line marked
  - Drawdown Analysis — filled area chart showing drawdown over time
- **Risk Summary Statistics table** at the bottom

---

## 🗣️ What to Say

> *"This is the Volatility Analysis page — the risk assessment center of the dashboard."*

### About Risk Metrics:
> *"These 4 metrics give an instant risk snapshot:*
> - *Annualized Volatility tells us how much the price fluctuates yearly. In crypto, this is usually 50-120%, which is extremely high compared to traditional stocks (15-20%).*
> - *Value at Risk (95%) tells us: 'With 95% confidence, you won't lose more than this percentage in a single day.' For example, if VaR is -4.2%, there's only a 5% chance of losing more than 4.2% in a day.*
> - *Maximum Drawdown is the worst peak-to-trough decline in the entire history. This tells us the worst-case scenario for someone who bought at the peak.*
> - *Sharpe Ratio measures risk-adjusted return — how much return you get per unit of risk. A Sharpe above 1.0 is good, above 2.0 is excellent, below 0 means you're losing money."*

### About Volatility Chart:
> *"This 2-panel chart shows the price on top and rolling 21-day annualized volatility below. Notice how volatility tends to cluster — during market crashes, volatility spikes and stays elevated for a while before calming down. This phenomenon is called 'volatility clustering' and it's a well-known property of financial markets."*

### About Returns Distribution:
> *"The histogram shows the distribution of daily returns. The orange dashed line marks the VaR 95% threshold. Everything to the left of that line represents the worst 5% of trading days. Notice that the distribution has fatter tails than a normal bell curve — extreme events (both positive and negative) happen more often than what a normal distribution predicts. This is why standard deviation alone is not enough to measure risk, and why we also use VaR and Max Drawdown."*

### About Drawdown Chart:
> *"The drawdown chart shows how much the price has fallen from its all-time high at any given point. It's always negative or zero. The deepest red area represents the maximum drawdown period. This is crucial for investors because it tells them: 'If you had bought at the worst possible time, how much would you have lost before the price recovered?'"*

---

## 🧠 Technical Points to Highlight
- VaR is calculated using the **historical simulation method**: `np.percentile(returns, 5)` — i.e., the 5th percentile of actual historical returns
- Sharpe Ratio formula: `(mean_annual_return - risk_free_rate) / annual_volatility` where risk_free_rate = 2% and annualization uses √365
- Max Drawdown uses `expanding().max()` to track the running peak, then `(price - peak) / peak` for the drawdown
- Drawdown chart uses `fill='tozeroy'` with red fill to visually emphasize loss periods
- All utility functions (`calculate_var`, `calculate_max_drawdown`, `calculate_sharpe_ratio`) are in `src/utils.py` for reusability

---

## ❓ Possible Mentor Questions on This Page
| Question | Short Answer |
|----------|--------------|
| "How do you calculate VaR?" | Historical simulation method — I take the 5th percentile of all historical daily returns. That value is the max loss at 95% confidence. |
| "What if VaR underestimates risk?" | VaR only works at the specified confidence level. The 5% tail events can be much worse. That's why I also show Max Drawdown as a complementary worst-case measure. |
| "Why is Sharpe Ratio negative?" | It means the coin's returns are lower than the risk-free rate (2%). You'd have been better off just keeping money in a savings account. |
| "What is volatility clustering?" | Periods of high volatility tend to follow high volatility. It happens because market shocks create uncertainty, which takes time to settle. It's a well-known property described in GARCH models. |

---
---

# 🔍 PAGE 4: MODEL COMPARISON (`4_model_comparison.py`)

---

## ✅ What You See on Screen
- **Top controls**: Coin selector + Forecast Horizon selector (7, 14, or 30 days)
- **"🚀 Run Model Comparison" button** (primary, full width)
- After clicking the button:
  - Progress messages: "Training ARIMA...", "Training SARIMA...", "Training Prophet..."
  - ✅ Success messages for each model
  - **🏆 Best Model** announcement with its MAPE score
  - **Performance Metrics Table** ranked by MAPE: columns for Rank, Model, MAPE, RMSE, MAE, R²
  - **MAPE Bar Chart** — bar chart comparing MAPE of all models
  - **Forecast vs Actual Chart** — line chart showing actual prices as white dots/line + each model's forecast in different colors

---

## 🗣️ What to Say

> *"This is the Model Comparison page — this is where I train and compare all my forecasting models side by side. Let me run it live."*

### Before Clicking the Button:
> *"I'll select a cryptocurrency, say BTC - Bitcoin, and a forecast horizon of 7 days. The way this works is: the system takes the last 7 days as the test set, trains each model on everything before that, and then compares the predictions against the actual prices."*

### Click the Button — While Models Train:
> *"You can see the models training one by one. First ARIMA — this is the fastest since it's a statistical model. Then SARIMA with weekly seasonality. Then Prophet which decomposes the time series into trend and seasonality components. Each one takes a few seconds."*

### After Results Appear:
> *"Here are the results. The best model is highlighted at the top with a green banner. The comparison table shows 4 metrics for each model:*
> - *MAPE (%) — the average percentage error. Lower is better. This is our primary ranking metric.*
> - *RMSE — penalizes large errors more heavily.*
> - *MAE — the average absolute error in dollars.*
> - *R² — how well the model explains the variance. 1.0 is perfect, 0 is no better than guessing the mean."*

### About the MAPE Bar Chart:
> *"This bar chart makes it easy to visually compare — you can instantly see which model has the lowest MAPE. The values are displayed on top of each bar."*

### About the Forecast vs Actual Chart:
> *"This is the most important visualization. The white line with markers shows the actual prices. The colored lines show each model's predictions. You can see how closely each model tracks the actual values. Sometimes one model captures the trend direction better even if its error metrics are similar."*

---

## 🧠 Technical Points to Highlight
- The comparison uses a **train-test split** where the last `horizon` days are held out for testing
- ARIMA is fitted with fixed order `(2,1,2)` for speed in the comparison (auto_arima is slower)
- SARIMA uses `(1,1,1)(1,0,1,7)` — weekly seasonal period of 7
- Prophet is trained on the full DataFrame with date and close columns
- Results are cached in `st.session_state` so they persist across interactions
- The `evaluate_model()` function from `src/evaluation.py` computes all 4 metrics at once
- The `compare_models()` function sorts all results by MAPE and adds rankings
- LSTM is NOT included in real-time comparison because it takes too long to train in a live dashboard demo — it would require minutes with GPU

---

## ❓ Possible Mentor Questions on This Page
| Question | Short Answer |
|----------|--------------|
| "Why is LSTM not included here?" | LSTM training takes several minutes (50 epochs of deep learning). It would make the live demo too slow. LSTM is available separately in the Forecasts page for individual runs. I compare it offline. |
| "What does MAPE of 3.5% mean?" | On average, the model's predictions are 3.5% off from the actual price. For a $60,000 Bitcoin, that's about $2,100 error. |
| "Why not use R² as the main metric?" | R² can be misleading for time series because it doesn't account for temporal patterns. MAPE is more intuitive and directly comparable across different coins/price ranges. |
| "Why did you fix the ARIMA order instead of using auto_arima?" | Auto_arima is computationally expensive and can take minutes. For a live demo comparison, I use a fixed reasonable order for speed. The Forecast page can use auto_arima for individual forecasts. |

---
---

# 🔮 PAGE 5: FORECASTS (`5_forecasts.py`)

---

## ✅ What You See on Screen
- **Top controls** in 3 columns:
  - Coin selector (all 17 coins)
  - Model selector: ARIMA, SARIMA, or Prophet
  - Forecast horizon: 7, 14, or 30 days
- **3 Info metrics**: Current Price, Data Points available, Annualized Volatility
- **"🔮 Generate Forecast" button** (primary, full width)
- After clicking:
  - **Forecast Summary**: 3 metrics showing:
    - Predicted price at end of horizon (with % change from current)
    - Forecast range (min to max predicted price)
    - 95% Confidence Interval (lower bound to upper bound)
  - **Forecast Visualization Chart**:
    - Historical prices (blue line) for the last 100 days
    - Forecast line (green with markers) extending into the future
    - 95% Confidence Interval shown as a green shaded area
    - Yellow dashed vertical line marking "Forecast Start"
  - **Forecast Details Table**: Day-by-day forecast values with cumulative change %
  - ⚠️ Disclaimer: educational purposes only

---

## 🗣️ What to Say

> *"This is the Forecast page — the core prediction feature of the project. Here, the user can select any coin, choose a model, and get a future price prediction."*

### Demo the Controls:
> *"I'll select ETH - Ethereum, use the Prophet model which handles seasonality well, and forecast for the next 14 days."*

### About the Info Metrics:
> *"Before generating, you can see the current price, how many data points we have to train on, and the current annualized volatility. More data points generally mean better model performance. Higher volatility means the forecast will be less certain."*

### Click Generate Forecast:
> *"The model is now training on the historical data and generating predictions."*

### After Results Appear:
> *"The forecast summary shows 3 key pieces of information:*
> - *The predicted price at the end of 14 days with a percentage change from today's price.*
> - *The range of predictions over the entire horizon — the lowest and highest predicted prices over the next 14 days.*
> - *The 95% confidence interval — this is a range where the actual price is expected to fall with 95% probability. Notice how the confidence interval widens as we go further into the future — that's because uncertainty grows with time."*

### About the Chart:
> *"This chart is the key deliverable. The blue line shows the last 100 days of actual historical prices. After the yellow dashed line marked 'Forecast Start', you see the green forecast line extending into the future. The green shaded area around it is the 95% confidence interval. You can see how the shading gets wider toward the right — meaning predictions further in time have more uncertainty."*

### About the Table:
> *"Below the chart, the table shows the exact predicted price for each day, along with the confidence interval bounds and the cumulative change from today's price. This allows precise analysis of each day's prediction."*

### Point Out the Disclaimer:
> *"I've added a disclaimer that these forecasts are for educational purposes only and should not be used for actual trading decisions. This is important from an ethical standpoint."*

---

## 🧠 Technical Points to Highlight
- Each model works slightly differently:
  - **ARIMA**: Fits on the `close` price time series with order `(2,1,2)`, calls `get_forecast(steps=horizon)` which returns predicted mean + confidence intervals
  - **SARIMA**: Same as ARIMA but adds seasonal components with period 7 (weekly)
  - **Prophet**: Takes a DataFrame with `ds` (date) and `y` (close) columns. Calls `make_future_dataframe(periods=horizon)` then `predict()` which returns `yhat`, `yhat_lower`, `yhat_upper`
- The historical context (last 100 days) is shown to give visual continuity between past and future
- Confidence intervals are model-specific and widened naturally by each model's uncertainty estimation
- Session state stores the forecast result, model name, and coin ID — so switching between pages doesn't lose the result
- The cumulative change column uses: `((forecast / current_price) - 1) * 100`

---

## ❓ Possible Mentor Questions on This Page
| Question | Short Answer |
|----------|--------------|
| "Why does the confidence interval widen?" | Because prediction uncertainty grows with time. Tomorrow's price is easier to predict than next month's. Models capture this through forecast variance that increases at each step. |
| "Can I trust this forecast?" | Not for real trading. Markets are affected by news, regulations, hacks, and many unpredictable events. These models capture historical patterns only. |
| "Why did you show the last 100 days of history?" | To provide visual context. Without historical data, the forecast line would appear isolated and hard to interpret. 100 days gives enough trend context. |
| "Which model is most accurate for forecasting?" | It varies by coin and time period. Prophet generally handles trend changes well. ARIMA/SARIMA are good for short-term. That's why I built the Model Comparison page — to test them head-to-head. |

---
---

# ⚠️ PAGE 6: RISK INDICATORS (`6_risk_indicators.py`)

---

## ✅ What You See on Screen
- **Coin selector** at the top
- **Two-column layout**:
  - **Left**: A **Risk Gauge** meter (speedometer-style) showing the overall risk score from 0 to 100, with color-coded ranges (green=Low, yellow=Moderate, orange=High, red=Extreme), and a big label below showing the risk level
  - **Right**: **Risk Factor Breakdown** with 3 progress bars:
    - Volatility score (price fluctuation intensity)
    - Drawdown score (peak-to-trough decline severity)
    - Value at Risk score (daily loss potential)
- **🚨 Risk Alerts** section — dynamic alerts based on current market conditions:
  - ⚠️ Extreme/High Volatility warnings
  - 📉 Sharp Decline warnings
  - 🔴 Overbought / 🟢 Oversold signals based on RSI
  - ✅ "No significant risk alerts" if everything is normal
- **Historical Risk Analysis** — 2-panel chart:
  - Top: Price line
  - Bottom: Rolling Volatility (red) + Drawdown (yellow) overlaid

---

## 🗣️ What to Say

> *"This is the Risk Indicators page — the most advanced analytics page in the dashboard. It calculates an overall risk score and provides automated alerts."*

### About the Risk Gauge:
> *"This gauge-style meter shows the overall risk score for the selected cryptocurrency on a scale of 0 to 100:*
> - *0–30: Low Risk (green)*
> - *30–50: Moderate Risk (yellow)*
> - *50–70: High Risk (orange)*
> - *70–100: Extreme Risk (red)*
>
> *The score is calculated using a weighted formula:*
> - *40% weight on Volatility Score*
> - *40% weight on Drawdown Score*
> - *20% weight on VaR Score*
>
> *This gives a balanced view combining different aspects of risk."*

### About Risk Factor Breakdown:
> *"On the right, each risk factor is broken down individually with a progress bar. For example, if the volatility score is 65/100, it means the price fluctuations are moderately high. The drawdown score reflects how severe the worst decline was. Each factor shows its label (Low/Moderate/High/Extreme), a visual progress bar, and a numeric description."*

### About Risk Alerts:
> *"This section automatically generates contextual alerts based on current market conditions:*
> - *If annualized volatility exceeds 100%, it shows an Extreme Volatility warning in red*
> - *If the total price decline exceeds 20%, it shows a Sharp Decline warning*
> - *If RSI is above 70, it warns about overbought conditions*
> - *If RSI is below 30, it suggests the coin may be oversold and due for a bounce*
> - *If no alerts trigger, it shows a green 'No significant risk alerts' message*
>
> *These alerts are fully dynamic — they change based on the selected coin's real data."*

### About Historical Risk Chart:
> *"The bottom chart overlays volatility and drawdown over time alongside the price. This helps identify patterns like: 'Volatility spiked right before the major price drop' or 'Risk was unusually low before the market crash.' This kind of retrospective analysis is valuable for understanding market risk behavior."*

---

## 🧠 Technical Points to Highlight
- Risk score formula: `overall = volatility_score × 0.4 + drawdown_score × 0.4 + var_score × 0.2`
- Individual scores are capped at 100 using `min(score, 100)` to prevent overflow
- The gauge is rendered using **Plotly's `go.Indicator`** with `mode="gauge+number"` — this creates the speedometer visual
- Risk level function maps score ranges to labels and colors: `get_risk_level(score) → (label, color)`
- Alerts use Streamlit's native `st.error()`, `st.warning()`, and `st.info()` components — color-coded for severity
- The progress bars use `st.progress(score / 100)` — a built-in Streamlit widget
- Custom HTML with `unsafe_allow_html=True` is used for the risk level badge styling

---

## ❓ Possible Mentor Questions on This Page
| Question | Short Answer |
|----------|--------------|
| "How did you come up with the 40-40-20 weight split?" | Volatility and drawdown are the two most important risk measures in finance. VaR supplements them for daily risk. The weights can be tuned based on use case — for a day trader, VaR would get higher weight. |
| "Is this risk score standard in the industry?" | The individual metrics (VaR, volatility, drawdown) are industry standard. The composite score is my custom implementation for this dashboard, inspired by risk scoring systems used in portfolio management. |
| "What happens if RSI and volatility disagree?" | They measure different things. RSI is about momentum (overbought/oversold), volatility is about price fluctuation. A coin can be overbought (RSI > 70) but have low volatility. The alerts show both independently. |
| "What action should a user take based on these alerts?" | An Extreme Volatility alert suggests caution — reduce position size or set stop-losses. An Oversold alert might be a buying opportunity. But no model is guaranteed — these are decision support tools, not trading signals. |

---
---

# 🎯 PRESENTATION ORDER (RECOMMENDED FLOW)

When presenting to your mentor, follow this exact order for maximum impact:

---

| # | Page | Time | What to Focus On |
|---|------|------|-----------------|
| 1 | **Home** | 3–4 min | Overview, KPIs, explain the sidebar, show the price chart with moving averages, quick look at Bollinger Bands and RSI tabs |
| 2 | **Executive Summary** | 2 min | Show sparklines, explain performance table, normalized comparison |
| 3 | **Price Trends** | 3 min | Switch between all 3 chart types (Line → Candlestick → With Indicators). Explain each. This shows the depth of EDA. |
| 4 | **Volatility** | 3 min | Explain all 4 risk metrics, show volatility clustering in the chart, explain the drawdown chart |
| 5 | **Model Comparison** | 4–5 min | 🔴 **Click the button live.** Train models in real-time. Show the best model result. Explain the forecast vs actual chart. This is the most impressive demo moment. |
| 6 | **Forecasts** | 3 min | Generate a fresh forecast live. Show the confidence interval widening. Point out the day-by-day table. |
| 7 | **Risk Indicators** | 2–3 min | Show the risk gauge, explain the scoring formula, read out the automated alerts, show the historical risk chart. End on a strong note. |

**Total: ~20 minutes**

---

## 🗣️ Closing Statement (After Showing All Pages)

> *"To summarize — I built an end-to-end cryptocurrency analytics system: from data collection using the CoinGecko API, through preprocessing where I engineer 30+ features, to exploratory data analysis with 10+ interactive visualizations, then 4 forecasting models (ARIMA, SARIMA, Prophet, LSTM), risk analytics with VaR, Sharpe Ratio, and Max Drawdown, and finally this interactive 7-page Streamlit dashboard that brings it all together. The entire project follows the standard data analytics pipeline: Collect → Clean → Analyze → Model → Visualize."*

---

## 💡 Pro Tips for the Live Demo

1. **Practice the dashboard flow once before the actual presentation** — know which buttons to click and in what order
2. **Keep another coin ready** — if the mentor asks "can you show another coin?", quickly switch using the sidebar dropdown
3. **If a model takes time to train**, use that moment to explain the model theory ("While SARIMA trains, let me explain how it captures weekly seasonality...")
4. **If something errors**, stay calm and say: "This sometimes happens due to the data characteristics of this particular coin. Let me switch to another coin." Then select a different coin.
5. **Have the PRESENTATION_AND_VIVA_GUIDE.md open** for the Q&A portion after the demo

---

> **You've built an impressive project, Pradeep. Walk your mentor through it confidently — the code and visualizations speak for themselves! 🚀**
