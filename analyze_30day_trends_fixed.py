"""
Verify and analyze the extended 30-day dataset
"""
import pandas as pd
import numpy as np
from datetime import datetime
from config import DATA_FILE

print("=" * 70)
print("EXTENDED DATASET ANALYSIS - 30 DAYS")
print("=" * 70)

# Load data
df = pd.read_csv(DATA_FILE)
df['Datetime'] = pd.to_datetime(df['Datetime'])

# Basic stats
print(f"\n[OK] Dataset loaded: {len(df):,} records")
print(f"\nTemporal Coverage:")
print(f"  Start: {df['Datetime'].min()}")
print(f"  End:   {df['Datetime'].max()}")
print(f"  Duration: {(df['Datetime'].max() - df['Datetime'].min()).days} days")
print(f"  Unique dates: {df['Datetime'].dt.date.nunique()}")

print(f"\nSymbols: {df['Symbol'].nunique()}")
symbols = sorted(df['Symbol'].unique())
print(f"  {', '.join(symbols)}")

# Calculate returns for each symbol
print(f"\n{'='*70}")
print("30-DAY RETURNS ANALYSIS")
print(f"{'='*70}")

returns_data = []
for symbol in symbols:
    sym_data = df[df['Symbol'] == symbol].sort_values('Datetime')
    if len(sym_data) > 0:
        first_price = sym_data['Close'].iloc[0]
        last_price = sym_data['Close'].iloc[-1]
        price_return = ((last_price - first_price) / first_price) * 100
        high_price = sym_data['High'].max()
        low_price = sym_data['Low'].min()
        volatility = sym_data['Close'].pct_change().std() * 100
        
        returns_data.append({
            'Symbol': symbol,
            'Start': f'${first_price:.2f}',
            'End': f'${last_price:.2f}',
            'Return %': f'{price_return:+.2f}%',
            'High': f'${high_price:.2f}',
            'Low': f'${low_price:.2f}',
            'Volatility %': f'{volatility:.2f}%'
        })

returns_df = pd.DataFrame(returns_data)
print("\n" + returns_df.to_string(index=False))

# Volume analysis
print(f"\n{'='*70}")
print("VOLUME & TREND ANALYSIS")
print(f"{'='*70}")

print(f"\nTotal trading volume: {df['Volume'].sum():,}")
print(f"Average volume: {df['Volume'].mean():,.0f}")
print(f"Max volume: {df['Volume'].max():,}")
print(f"Min volume: {df['Volume'].min():,}")

# Daily volume trends
print(f"\nDaily volume pattern:")
df['Date'] = df['Datetime'].dt.date
daily_vol = df.groupby('Date')['Volume'].sum()
print(f"  Average daily volume: {daily_vol.mean():,.0f}")
print(f"  Peak daily volume: {daily_vol.max():,.0f}")
print(f"  Low daily volume: {daily_vol.min():,.0f}")

# Sentiment analysis
print(f"\n{'='*70}")
print("SENTIMENT ANALYSIS")
print(f"{'='*70}")

print(f"\nAverage sentiment: {df['Sentiment'].mean():.1f}/100")
print(f"Sentiment range: {df['Sentiment'].min()}-{df['Sentiment'].max()}")
print(f"Std deviation: {df['Sentiment'].std():.2f}")

# Daily sentiment trend
daily_sentiment = df.groupby('Date')['Sentiment'].mean()
print(f"Day 1 sentiment: {daily_sentiment.iloc[0]:.1f}/100")
print(f"Day 30 sentiment: {daily_sentiment.iloc[-1]:.1f}/100")

# Top performers
print(f"\n{'='*70}")
print("TOP & BOTTOM PERFORMERS (30-day)")
print(f"{'='*70}")

symbol_returns = []
for symbol in symbols:
    sym_data = df[df['Symbol'] == symbol].sort_values('Datetime')
    first = sym_data['Close'].iloc[0]
    last = sym_data['Close'].iloc[-1]
    ret = ((last - first) / first) * 100
    symbol_returns.append((symbol, ret))

symbol_returns.sort(key=lambda x: x[1], reverse=True)
print("\nTop 5 gainers:")
for i, (sym, ret) in enumerate(symbol_returns[:5], 1):
    print(f"  {i}. {sym}: {ret:+.2f}%")

print("\nTop 5 losers:")
for i, (sym, ret) in enumerate(symbol_returns[-5:], 1):
    print(f"  {i}. {sym}: {ret:+.2f}%")

print(f"\n{'='*70}")
print("DATASET READY FOR ANALYSIS")
print(f"{'='*70}")
print("\nYou can now:")
print("  - Analyze 30-day trends and price movements")
print("  - Calculate daily/hourly returns")
print("  - Study volatility patterns")
print("  - Compare cryptocurrency performance")
print("  - Build predictive models")
print("  - View trends in the Streamlit dashboard!")
