#!/usr/bin/env python3
"""Generate dashboard visualization images from 30-day cryptocurrency data."""

import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

sys.path.insert(0, '.')
import config

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['figure.figsize'] = (14, 8)

# Create figures directory if it doesn't exist
os.makedirs('figures', exist_ok=True)

print("Generating dashboard visualization images...")
print("=" * 70)

# Load data
df = pd.read_csv(config.DATA_FILE)
df['Datetime'] = pd.to_datetime(df['Datetime'])
df = df.sort_values('Datetime')

# Get 30-day stats
print(f"Dataset: {len(df)} records from {df['Datetime'].min()} to {df['Datetime'].max()}")

# 1. TOP PERFORMERS - 30-Day Returns
print("\n[1] Generating: 30-Day Returns Chart...")
fig, ax = plt.subplots(figsize=(12, 8))

returns = {}
for symbol in df['Symbol'].unique():
    sym_data = df[df['Symbol'] == symbol].sort_values('Datetime')
    if len(sym_data) > 0:
        first_price = sym_data['Close'].iloc[0]
        last_price = sym_data['Close'].iloc[-1]
        ret = ((last_price - first_price) / first_price) * 100
        returns[symbol] = ret

returns_sorted = dict(sorted(returns.items(), key=lambda x: x[1], reverse=True))
colors = ['green' if v > 0 else 'red' for v in returns_sorted.values()]

ax.barh(list(returns_sorted.keys()), list(returns_sorted.values()), color=colors, alpha=0.7, edgecolor='black')
ax.set_xlabel('30-Day Return (%)', fontsize=12, fontweight='bold')
ax.set_title('30-Day Cryptocurrency Returns', fontsize=14, fontweight='bold', pad=20)
ax.axvline(x=0, color='black', linestyle='-', linewidth=0.8)
ax.grid(axis='x', alpha=0.3)

for i, v in enumerate(returns_sorted.values()):
    label = f"{v:.1f}%"
    ax.text(v + (1 if v > 0 else -1), i, label, va='center', ha='left' if v > 0 else 'right', fontweight='bold')

plt.tight_layout()
plt.savefig('figures/01_30day_returns.png', dpi=300, bbox_inches='tight')
print("   ✓ Saved: 01_30day_returns.png")
plt.close()

# 2. PRICE TRENDS - Top 5 performers
print("[2] Generating: Price Trends Chart (Top 5)...")
fig, ax = plt.subplots(figsize=(14, 8))

top_5 = list(returns_sorted.keys())[:5]
colors_palette = sns.color_palette("husl", len(top_5))

for symbol, color in zip(top_5, colors_palette):
    sym_data = df[df['Symbol'] == symbol].sort_values('Datetime')
    normalized_price = (sym_data['Close'] / sym_data['Close'].iloc[0] - 1) * 100
    ax.plot(sym_data['Datetime'], normalized_price, label=symbol, linewidth=2.5, color=color, marker='o', markersize=3, alpha=0.8)

ax.set_xlabel('Date', fontsize=12, fontweight='bold')
ax.set_ylabel('Price Change (%)', fontsize=12, fontweight='bold')
ax.set_title('30-Day Price Trends - Top 5 Performers', fontsize=14, fontweight='bold', pad=20)
ax.legend(loc='best', fontsize=11, framealpha=0.9)
ax.grid(True, alpha=0.3)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('figures/02_price_trends.png', dpi=300, bbox_inches='tight')
print("   ✓ Saved: 02_price_trends.png")
plt.close()

# 3. VOLATILITY COMPARISON
print("[3] Generating: Volatility Comparison Chart...")
fig, ax = plt.subplots(figsize=(12, 8))

volatility = {}
for symbol in df['Symbol'].unique():
    sym_data = df[df['Symbol'] == symbol].sort_values('Datetime')
    daily_returns = sym_data['Close'].pct_change() * 100
    volatility[symbol] = daily_returns.std()

vol_sorted = dict(sorted(volatility.items(), key=lambda x: x[1], reverse=True))
colors = plt.cm.RdYlGn_r(np.linspace(0.3, 0.7, len(vol_sorted)))

ax.bar(vol_sorted.keys(), vol_sorted.values(), color=colors, alpha=0.7, edgecolor='black')
ax.set_ylabel('Volatility (Daily Return Std Dev %)', fontsize=12, fontweight='bold')
ax.set_title('30-Day Volatility Comparison', fontsize=14, fontweight='bold', pad=20)
ax.grid(axis='y', alpha=0.3)
plt.xticks(rotation=45, ha='right')

for i, (symbol, vol) in enumerate(vol_sorted.items()):
    ax.text(i, vol + 0.05, f'{vol:.2f}%', ha='center', va='bottom', fontsize=9, fontweight='bold')

plt.tight_layout()
plt.savefig('figures/03_volatility.png', dpi=300, bbox_inches='tight')
print("   ✓ Saved: 03_volatility.png")
plt.close()

# 4. DAILY VOLUME HEATMAP
print("[4] Generating: Daily Volume Heatmap...")
fig, ax = plt.subplots(figsize=(14, 8))

# Pivot for heatmap
volume_pivot = df.pivot_table(values='Volume', index='Symbol', columns=df['Datetime'].dt.date, aggfunc='mean')
volume_pivot_normalized = (volume_pivot - volume_pivot.min().min()) / (volume_pivot.max().max() - volume_pivot.min().min())

sns.heatmap(volume_pivot_normalized, cmap='YlOrRd', cbar_kws={'label': 'Normalized Volume'}, ax=ax)
ax.set_title('30-Day Trading Volume Heatmap (Daily Average)', fontsize=14, fontweight='bold', pad=20)
ax.set_xlabel('Date', fontsize=12, fontweight='bold')
ax.set_ylabel('Cryptocurrency', fontsize=12, fontweight='bold')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('figures/04_volume_heatmap.png', dpi=300, bbox_inches='tight')
print("   ✓ Saved: 04_volume_heatmap.png")
plt.close()

# 5. CORRELATION HEATMAP
print("[5] Generating: Price Correlation Heatmap...")
fig, ax = plt.subplots(figsize=(12, 10))

# Get latest price for each symbol to calculate correlations
latest_prices = df.sort_values('Datetime').groupby('Symbol')['Close'].last()
first_prices = df.sort_values('Datetime').groupby('Symbol')['Close'].first()
returns_series = ((latest_prices - first_prices) / first_prices * 100)

# Alternative: Get daily returns correlation
daily_returns = df.pivot_table(values='Close', index='Datetime', columns='Symbol').pct_change() * 100
corr_matrix = daily_returns.corr()

sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', center=0, 
            cbar_kws={'label': 'Correlation'}, ax=ax, square=True, linewidths=0.5)
ax.set_title('30-Day Daily Returns Correlation Matrix', fontsize=14, fontweight='bold', pad=20)
plt.xticks(rotation=45, ha='right')
plt.yticks(rotation=0)
plt.tight_layout()
plt.savefig('figures/05_correlation.png', dpi=300, bbox_inches='tight')
print("   ✓ Saved: 05_correlation.png")
plt.close()

# 6. OHLC CANDLESTICK - Top performer (e.g., DOGE)
print("[6] Generating: OHLC Candlestick Chart (DOGE)...")
fig, ax = plt.subplots(figsize=(14, 8))

top_symbol = list(returns_sorted.keys())[0]
sym_data = df[df['Symbol'] == top_symbol].sort_values('Datetime')

# Weekly candles for clarity
sym_data['Week'] = sym_data['Datetime'].dt.isocalendar().week
weekly = sym_data.groupby('Week').agg({
    'Open': 'first',
    'High': 'max',
    'Low': 'min',
    'Close': 'last',
    'Datetime': 'first'
}).reset_index()

width = 0.6
width2 = 0.05

for idx, row in weekly.iterrows():
    date = row['Datetime']
    open_price = row['Open']
    close_price = row['Close']
    high_price = row['High']
    low_price = row['Low']
    
    color = 'green' if close_price >= open_price else 'red'
    
    # High-Low line
    ax.plot([idx, idx], [low_price, high_price], color=color, linewidth=2)
    
    # Open-Close rectangle
    height = abs(close_price - open_price)
    bottom = min(open_price, close_price)
    rect = plt.Rectangle((idx - width/2, bottom), width, height, 
                          facecolor=color, edgecolor=color, alpha=0.8)
    ax.add_patch(rect)

ax.set_xlabel('Week', fontsize=12, fontweight='bold')
ax.set_ylabel('Price (USD)', fontsize=12, fontweight='bold')
ax.set_title(f'{top_symbol}: 30-Day Weekly OHLC Candlestick Chart', fontsize=14, fontweight='bold', pad=20)
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('figures/06_ohlc_candles.png', dpi=300, bbox_inches='tight')
print("   ✓ Saved: 06_ohlc_candles.png")
plt.close()

# 7. DISTRIBUTION ANALYSIS
print("[7] Generating: Returns Distribution Chart...")
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
axes = axes.flatten()

top_4 = list(returns_sorted.keys())[:4]
for idx, symbol in enumerate(top_4):
    sym_data = df[df['Symbol'] == symbol].sort_values('Datetime')
    daily_ret = sym_data['Close'].pct_change().dropna() * 100
    
    axes[idx].hist(daily_ret, bins=20, color='steelblue', alpha=0.7, edgecolor='black')
    axes[idx].axvline(daily_ret.mean(), color='red', linestyle='--', linewidth=2, label=f'Mean: {daily_ret.mean():.2f}%')
    axes[idx].set_title(f'{symbol} - Daily Returns Distribution', fontweight='bold')
    axes[idx].set_xlabel('Daily Return (%)', fontsize=10)
    axes[idx].set_ylabel('Frequency', fontsize=10)
    axes[idx].legend()
    axes[idx].grid(True, alpha=0.3)

plt.suptitle('Daily Returns Distribution - Top 4 Performers', fontsize=14, fontweight='bold', y=1.00)
plt.tight_layout()
plt.savefig('figures/07_returns_distribution.png', dpi=300, bbox_inches='tight')
print("   ✓ Saved: 07_returns_distribution.png")
plt.close()

# 8. CUMULATIVE RETURNS
print("[8] Generating: Cumulative Returns Chart...")
fig, ax = plt.subplots(figsize=(14, 8))

colors_palette = sns.color_palette("husl", len(df['Symbol'].unique()))
for symbol, color in zip(df['Symbol'].unique(), colors_palette):
    sym_data = df[df['Symbol'] == symbol].sort_values('Datetime')
    cum_returns = (1 + sym_data['Close'].pct_change()).cumprod() - 1
    ax.plot(sym_data['Datetime'], cum_returns * 100, label=symbol, linewidth=1.5, color=color, alpha=0.7)

ax.set_xlabel('Date', fontsize=12, fontweight='bold')
ax.set_ylabel('Cumulative Return (%)', fontsize=12, fontweight='bold')
ax.set_title('30-Day Cumulative Returns - All Cryptocurrencies', fontsize=14, fontweight='bold', pad=20)
ax.legend(loc='best', fontsize=8, ncol=3, framealpha=0.9)
ax.grid(True, alpha=0.3)
ax.axhline(y=0, color='black', linestyle='-', linewidth=0.8)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('figures/08_cumulative_returns.png', dpi=300, bbox_inches='tight')
print("   ✓ Saved: 08_cumulative_returns.png")
plt.close()

print("\n" + "=" * 70)
print("✅ All 8 dashboard visualization images generated successfully!")
print("   Location: figures/ directory")
print("   - 01_30day_returns.png")
print("   - 02_price_trends.png")
print("   - 03_volatility.png")
print("   - 04_volume_heatmap.png")
print("   - 05_correlation.png")
print("   - 06_ohlc_candles.png")
print("   - 07_returns_distribution.png")
print("   - 08_cumulative_returns.png")
print("\nReady for dashboard documentation and README updates.")
