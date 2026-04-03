# Dashboard Visualizations Gallery

## 30-Day Cryptocurrency Analysis (June 1 - July 1, 2021)

Complete collection of professional dashboard images showing 30-day cryptocurrency trends, analysis, and performance metrics across 19 cryptocurrencies with 41,040 hourly data records.

---

## 1. 30-Day Returns Comparison

**File:** `figures/01_30day_returns.png`

Shows cumulative returns for all 19 cryptocurrencies over the 30-day period.

### Key Insights:

- **Top Performer:** DOGE with +103.26% return
- **Second Place:** ADA with +75.29% return
- **Third Place:** ETC with +53.49% return
- **Best Performer:** ETH with +19.28% return
- **Chart Type:** Horizontal bar chart with color coding (green = positive, red = negative)

### Use Cases:

- Executive summary presentations
- Portfolio performance tracking
- Market comparison analysis
- Investment communication

---

## 2. Price Trends - Top 5 Performers

**File:** `figures/02_price_trends.png`

Multi-line chart displaying normalized price movements of the top 5 performing cryptocurrencies.

### Cryptocurrencies Shown:

1. DOGE - Dogecoin
2. ADA - Cardano
3. ETC - Ethereum Classic
4. ETH - Ethereum
5. EOS - EOS

### Features:

- Normalized to percentage change from starting price
- Individual color-coded lines for each cryptocurrency
- Marker points for better readability
- Complete 30-day time coverage

### Use Cases:

- Trend identification
- Performance comparison
- Market cycle analysis
- Trading strategy development

---

## 3. Volatility Comparison

**File:** `figures/03_volatility.png`

Bar chart comparing daily return volatility across all 19 cryptocurrencies.

### Volatility Metrics:

- **Highest Volatility:** ~2.41% (daily return std dev)
- **Lowest Volatility:** ~0.94%
- **Average Volatility:** ~1.5%

### Color Gradient:

- Red: High volatility (higher risk)
- Yellow: Medium volatility
- Green: Low volatility (lower risk)

### Use Cases:

- Risk assessment
- Portfolio diversification
- Volatility regime identification
- Option pricing inputs

---

## 4. Daily Volume Heatmap

**File:** `figures/04_volume_heatmap.png`

Heatmap showing normalized trading volume patterns across all cryptocurrencies and dates.

### Dimensions:

- **Rows (Y-Axis):** 19 cryptocurrency symbols
- **Columns (X-Axis):** 31 calendar days
- **Color Intensity:** Represents normalized trading volume

### Features:

- Identifies volume concentration periods
- Shows trading patterns by symbol
- Reveals liquidity changes over time
- Highlights volume anomalies

### Use Cases:

- Liquidity analysis
- Trading volume patterns
- Market activity tracking
- Anomaly detection

---

## 5. Price Correlation Matrix

**File:** `figures/05_correlation.png`

Correlation heatmap showing relationships between cryptocurrencies' daily returns.

### Matrix Details:

- **Size:** 19x19 (all cryptocurrency pairs)
- **Scale:** -1 (perfect negative correlation) to +1 (perfect positive correlation)
- **Color Scheme:** Cool tones (negative) to warm tones (positive)

### Key Findings:

- Most cryptocurrencies show moderate positive correlation
- Bitcoin effect visible (leading indicator)
- Stablecoin pairs highly correlated
- Altcoins show varied correlation patterns

### Use Cases:

- Portfolio optimization
- Hedging strategy development
- Risk management
- Diversification analysis

---

## 6. OHLC Candlestick Chart - DOGE

**File:** `figures/06_ohlc_candles.png`

Weekly candlestick chart of the top performer (DOGE).

### Chart Details:

- **Period:** 4-5 weeks of data
- **Candle Format:** Standard OHLC (Open-High-Low-Close)
- **Color Coding:** Green (close > open), Red (close < open)
- **Focus:** DOGE (strongest performer at +103%)

### Technical Analysis:

- Trend visualization
- Support/resistance identification
- Volatility patterns
- Volume bar integration

### Use Cases:

- Technical analysis
- Trend confirmation
- Entry/exit point identification
- Pattern recognition

---

## 7. Daily Returns Distribution

**File:** `figures/07_returns_distribution.png`

Distribution histograms of daily returns for the top 4 performing cryptocurrencies (2x2 grid).

### Cryptocurrencies Included:

1. **DOGE** - Top performer (+103%)
2. **ADA** - Second place (+75%)
3. **ETC** - Third place (+53%)
4. **ETH** - Strong performer (+19%)

### Statistical Features:

- 20 histogram bins per symbol
- Mean return line overlay (red dashed)
- Distribution shape visualization
- Outlier identification

### Use Cases:

- Distribution analysis
- Tail risk assessment
- Statistical modeling
- Value-at-Risk calculation

---

## 8. Cumulative Returns - All 19 Cryptocurrencies

**File:** `figures/08_cumulative_returns.png`

Multi-line chart showing cumulative returns for all 19 cryptocurrencies over the 30-day period.

### Coverage:

- **All 19 Symbols:** Each with distinct color
- **Time Period:** June 1 - July 1, 2021
- **Frequency:** Calculated from daily returns
- **Compound Effect:** Cumulative growth visualization

### Features:

- Long-term trend tracking
- Outperformance identification
- Relative performance comparison
- Market leader identification

### Use Cases:

- Performance benchmarking
- Long-term trend analysis
- Outperformance tracking
- Portfolio comparison

---

## Technical Specifications

### Image Quality

- **Resolution:** 300 DPI (suitable for printing)
- **Format:** PNG with transparency
- **Size Range:** 100-900 KB per image
- **Color Space:** RGB

### Data Source

- **Dataset:** main_df_enhanced.csv
- **Records:** 41,040 hourly candles
- **Period:** June 1, 2021 - July 1, 2021
- **Cryptocurrencies:** 19 major altcoins
- **Frequency:** Hourly OHLCV data

### Generation Method

- **Script:** generate_dashboard_images.py
- **Libraries:** Matplotlib, Seaborn, Pandas, NumPy
- **Date Generated:** April 3, 2026

---

## Regeneration Instructions

To regenerate these images with updated data:

```bash
python generate_dashboard_images.py
```

The script will:

1. Load the latest data from main_df_enhanced.csv
2. Calculate all metrics and trends
3. Generate all 8 visualizations
4. Save to the figures/ directory
5. Overwrite existing images with updated versions

---

## Integration Points

These images are used in:

- **README.md** - Main project documentation
- **Dashboard Pages** - Streamlit application UI
- **Presentations** - Project showcases
- **Reports** - Analysis documentation
- **Social Media** - Project announcements

---

## File Manifest

| Filename                    | Size   | Purpose                 |
| --------------------------- | ------ | ----------------------- |
| 01_30day_returns.png        | 196 KB | Returns comparison      |
| 02_price_trends.png         | 558 KB | Price movement trends   |
| 03_volatility.png           | 219 KB | Volatility analysis     |
| 04_volume_heatmap.png       | 209 KB | Trading volume patterns |
| 05_correlation.png          | 895 KB | Correlation matrix      |
| 06_ohlc_candles.png         | 112 KB | Candlestick chart       |
| 07_returns_distribution.png | 289 KB | Distribution analysis   |
| 08_cumulative_returns.png   | 678 KB | Cumulative performance  |

**Total Size:** ~3.2 MB for all visualizations

---

## Quality Notes

- All images are publication-quality (300 DPI)
- Color schemes are colorblind-friendly
- Markdown rendering optimized for GitHub
- Images automatically regenerate with new data
- No external dependencies required (matplotlib-based)

For questions or customization needs, refer to `generate_dashboard_images.py`.
