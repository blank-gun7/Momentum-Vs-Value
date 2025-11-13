"""
Momentum vs Value Factor Analysis - Starter Code
Course: Data Sciences Assignment
Time: 3 hours total

This starter code provides the structure for your analysis.
Copy each section into separate Jupyter notebook cells.
"""

# %% [markdown]
# # Momentum vs Value Factor Performance Analysis (2024)
# ## Statistical Study of Indian Stock Market Returns
#
# ### Statistical Framework:
# - **Data Analysis:** Types, organization, visualization, interpretation
# - **Probability Theory:** Distributions and random variables
# - **Statistical Inference:** Sampling, estimation, hypothesis testing

# %% [markdown]
# ## Story 1.1: Project Setup and Data Loading (15 mins)

# %%
# Import required libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings

warnings.filterwarnings('ignore')

# Set style and random seed for reproducibility
sns.set_style('whitegrid')
np.random.seed(42)

print("Libraries imported successfully!")


# Helper: normalize tickers so price & fundamentals match
def normalize_ticker(s):
    """
    Put all tickers into a common, clean format so that
    price_data and fundamentals can be matched.
    Examples:
    - 'ADANIPORTS.NS' -> 'ADANIPORTS'
    - 'SBIN-EQ'       -> 'SBIN'
    """
    s = str(s).upper().strip()

    # Remove common exchange suffixes
    for suffix in ['.NS', '.NSE', '.BSE', '.BO']:
        if s.endswith(suffix):
            s = s[: -len(suffix)]

    # Remove common series suffixes
    for suffix in ['-EQ', '-BE', '-BL', '-BZ']:
        if s.endswith(suffix):
            s = s[: -len(suffix)]

    # Extra cleanup of stray spaces
    s = s.strip()
    return s


# %% [markdown]
# ### Load the Kaggle Datasets
# 1. Indian Stock Market Data 2015–2024 (Neeraj Vantagudi)
# 2. BSE,NSE STOCK FUNDAMENTALS RATIOS

# %%
# Load price data
# ✅ Replace with your actual file path if different
price_data = pd.read_csv('Datasets/stock_price_dataset/Stock_Data.csv')
print(f"Price data shape (raw): {price_data.shape}")
print(f"Price data columns (raw): {price_data.columns.tolist()}")
print(price_data.head())

# Ensure we have a consistent Date column name
date_candidates = ['Date', 'date', 'DATE']
date_col = None
for c in date_candidates:
    if c in price_data.columns:
        date_col = c
        break
if date_col is None:
    raise ValueError("Could not find a date column in price_data.")
if date_col != 'Date':
    price_data.rename(columns={date_col: 'Date'}, inplace=True)

# Ensure we have a consistent stock identifier column in price data
price_stock_candidates = ['Stock', 'STOCK', 'Symbol', 'SYMBOL', 'Ticker', 'TICKER']
price_stock_col = None
for c in price_stock_candidates:
    if c in price_data.columns:
        price_stock_col = c
        break
if price_stock_col is None:
    raise ValueError("Could not find a stock identifier column in price_data.")
if price_stock_col != 'Stock':
    price_data.rename(columns={price_stock_col: 'Stock'}, inplace=True)

print(f"Price data columns (after renaming): {price_data.columns.tolist()}")


# %%
# Load fundamentals data
# ✅ Replace with your actual file path if different
fundamentals = pd.read_csv('Datasets/FUNDAMENTALratios.csv')
print(f"Fundamentals shape (raw): {fundamentals.shape}")
print(f"Fundamentals columns (raw): {fundamentals.columns.tolist()}")
print(fundamentals.head())

# Ensure we have a consistent stock identifier column in fundamentals
fund_stock_candidates = ['symbol', 'SYMBOL', 'Symbol', 'Ticker', 'TICKER']
fund_symbol_col = None
for c in fund_stock_candidates:
    if c in fundamentals.columns:
        fund_symbol_col = c
        break
if fund_symbol_col is None:
    raise ValueError("Could not find a stock identifier column in fundamentals.")
if fund_symbol_col != 'symbol':
    fundamentals.rename(columns={fund_symbol_col: 'symbol'}, inplace=True)

# Ensure we have a P/E column (value factor)
pe_candidates = ['trailingPE', 'P/E', 'PE', 'P_E', 'PE_RATIO']
pe_col = None
for c in pe_candidates:
    if c in fundamentals.columns:
        pe_col = c
        break
if pe_col is None:
    raise ValueError("Could not find a P/E-related column in fundamentals.")
if pe_col != 'trailingPE':
    fundamentals.rename(columns={pe_col: 'trailingPE'}, inplace=True)

print(f"Fundamentals columns (after renaming): {fundamentals.columns.tolist()}")

# %% [markdown]
# ## Story 1.2: Data Cleaning and Integration (20 mins)
# Filter to 2023-2024 period and merge datasets

# %%
# Convert date column to datetime
price_data['Date'] = pd.to_datetime(price_data['Date'])

# Filter to 2023-2024 period
price_filtered = price_data[price_data['Date'].dt.year.isin([2023, 2024])].copy()
print(f"Filtered price data: {price_filtered.shape}")
if not price_filtered.empty:
    print(f"Date range: {price_filtered['Date'].min()} to {price_filtered['Date'].max()}")
else:
    print("WARNING: No rows found for years 2023 or 2024 in price data.")

# Normalize tickers in BOTH datasets so they live in the same space
price_filtered['Stock'] = price_filtered['Stock'].apply(normalize_ticker)
fundamentals['symbol'] = fundamentals['symbol'].apply(normalize_ticker)

# Check for matching stocks between datasets
price_stocks = price_filtered['Stock'].dropna().unique()
fundamental_stocks = fundamentals['symbol'].dropna().unique()

common_stocks = set(price_stocks) & set(fundamental_stocks)

print(f"Stocks in price data (unique): {len(price_stocks)}")
print(f"Stocks in fundamentals (unique): {len(fundamental_stocks)}")
print(f"Common stocks after normalization: {len(common_stocks)}")

# Optional: show a few examples
print("Sample price tickers:", list(sorted(price_stocks))[:10])
print("Sample fundamentals tickers:", list(sorted(fundamental_stocks))[:10])
print("Sample common tickers:", list(sorted(common_stocks))[:10])

if len(common_stocks) == 0:
    raise ValueError(
        "After normalizing tickers, there are still 0 common stocks between "
        "price data and fundamentals. Check that you're using matching universes "
        "and correct CSV files."
    )

# Filter to common stocks
price_filtered = price_filtered[price_filtered['Stock'].isin(common_stocks)]
fundamentals_filtered = fundamentals[fundamentals['symbol'].isin(common_stocks)].copy()

# %% [markdown]
# ## Story 1.3: Factor Calculation (20 mins)
# Calculate momentum (2023) and extract value metrics

# %%
# Calculate 2023 momentum for each stock
def calculate_momentum(df, year=2023):
    """Calculate momentum as (end_price - start_price) / start_price"""
    year_data = df[df['Date'].dt.year == year].copy()

    momentum_dict = {}
    for stock in year_data['Stock'].unique():
        stock_data = year_data[year_data['Stock'] == stock].sort_values('Date')
        if len(stock_data) > 0:
            # Use first and last available prices
            start_price = stock_data['Close'].iloc[0]
            end_price = stock_data['Close'].iloc[-1]
            if start_price != 0:
                momentum = (end_price - start_price) / start_price
                momentum_dict[stock] = momentum

    return pd.DataFrame.from_dict(momentum_dict, orient='index', columns=['momentum_2023'])


momentum_df = calculate_momentum(price_filtered, 2023)
print(f"Calculated momentum for {len(momentum_df)} stocks")
print(momentum_df.describe())

# %%
# Calculate 2024 returns
returns_2024 = calculate_momentum(price_filtered, 2024)
returns_2024.columns = ['return_2024']

print(f"Calculated 2024 returns for {len(returns_2024)} stocks")

# Extract P/E ratios from fundamentals (value factor)
pe_data = fundamentals_filtered[['symbol', 'trailingPE']].copy()
pe_data.columns = ['Stock', 'pe_ratio_2023']
pe_data = pe_data.set_index('Stock')

# Combine all factors
analysis_df = momentum_df.join(pe_data).join(returns_2024)
analysis_df = analysis_df.dropna()

# Filter to positive P/E only (value stocks should have positive P/E)
analysis_df = analysis_df[analysis_df['pe_ratio_2023'] > 0]

print(f"Final analysis dataset: {len(analysis_df)} stocks")
print(analysis_df.head())

if analysis_df.empty:
    raise ValueError(
        "The final analysis_df is empty after merging momentum, P/E, and returns.\n"
        "Possible reasons:\n"
        "- No 2024 data in price file\n"
        "- P/E missing or non-positive for all common stocks\n"
        "- Path / file mismatch. Re-check your CSVs."
    )

# %% [markdown]
# ## Story 1.4: Exploratory Data Analysis (15 mins)

# %%
# Summary statistics
print("=== Summary Statistics (Descriptive Analysis) ===")
print(analysis_df.describe())

# %%
# Create visualizations
fig, axes = plt.subplots(2, 3, figsize=(15, 8))

# Histograms (Data Visualization)
axes[0, 0].hist(analysis_df['momentum_2023'], bins=20, edgecolor='black')
axes[0, 0].set_title('Momentum Distribution (2023)')
axes[0, 0].set_xlabel('Momentum')

axes[0, 1].hist(analysis_df['pe_ratio_2023'], bins=20, edgecolor='black')
axes[0, 1].set_title('P/E Ratio Distribution (2023)')
axes[0, 1].set_xlabel('P/E Ratio')

axes[0, 2].hist(analysis_df['return_2024'], bins=20, edgecolor='black')
axes[0, 2].set_title('Returns Distribution (2024)')
axes[0, 2].set_xlabel('Returns')

# Scatter plots (Bivariate Analysis)
axes[1, 0].scatter(analysis_df['momentum_2023'], analysis_df['return_2024'], alpha=0.5)
axes[1, 0].set_xlabel('Momentum 2023')
axes[1, 0].set_ylabel('Return 2024')
axes[1, 0].set_title('Momentum vs Returns')

axes[1, 1].scatter(analysis_df['pe_ratio_2023'], analysis_df['return_2024'], alpha=0.5)
axes[1, 1].set_xlabel('P/E Ratio 2023')
axes[1, 1].set_ylabel('Return 2024')
axes[1, 1].set_title('P/E vs Returns')

# Correlation heatmap
corr_matrix = analysis_df.corr(numeric_only=True)
sns.heatmap(corr_matrix, annot=True, fmt='.2f', ax=axes[1, 2])
axes[1, 2].set_title('Correlation Matrix')

plt.tight_layout()
plt.show()

# %% [markdown]
# ## Story 1.5: Probability Modeling (15 mins)

# %%
# Model returns as random variables
returns = analysis_df['return_2024']

print("=== Probability Concepts (Random Variables & Distributions) ===")
print(f"Expected Value (Mean) of Returns: {returns.mean():.4f}")
print(f"Variance of Returns: {returns.var():.4f}")
print(f"Standard Deviation: {returns.std():.4f}")
print(f"Skewness: {stats.skew(returns):.4f}")
print(f"Kurtosis: {stats.kurtosis(returns):.4f}")

# %%
# Test for normality and visualize
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Histogram with normal overlay
axes[0].hist(returns, bins=20, density=True, alpha=0.7, edgecolor='black')
mu, std = returns.mean(), returns.std()
xmin, xmax = axes[0].get_xlim()
x = np.linspace(xmin, xmax, 100)
p = stats.norm.pdf(x, mu, std)
axes[0].plot(x, p, 'r-', linewidth=2, label='Normal Distribution')
axes[0].set_title('Returns Distribution vs Normal')
axes[0].set_xlabel('Returns')
axes[0].set_ylabel('Probability Density')
axes[0].legend()

# Q-Q plot
stats.probplot(returns, dist="norm", plot=axes[1])
axes[1].set_title('Q-Q Plot (Testing Normality)')

plt.tight_layout()
plt.show()

# Shapiro-Wilk test
if len(returns) >= 3:
    stat, p_value = stats.shapiro(returns)
    print(f"\nShapiro-Wilk Test for Normality:")
    print(f"Test Statistic: {stat:.4f}")
    print(f"P-value: {p_value:.4f}")
    print(f"Conclusion: {'Reject' if p_value < 0.05 else 'Fail to reject'} null hypothesis of normality")
else:
    p_value = np.nan
    print("\nShapiro-Wilk Test for Normality:")
    print("Not enough observations (need at least 3) to run Shapiro-Wilk test.")

# %% [markdown]
# ## Story 1.6: Portfolio Construction (20 mins)

# %%
# Create quintile portfolios
analysis_df['momentum_quintile'] = pd.qcut(
    analysis_df['momentum_2023'],
    q=5,
    labels=['Q1_Low', 'Q2', 'Q3', 'Q4', 'Q5_High'],
    duplicates='drop'   # avoid bin edge duplication error
)

analysis_df['value_quintile'] = pd.qcut(
    analysis_df['pe_ratio_2023'],
    q=5,
    labels=['Q1_Value', 'Q2', 'Q3', 'Q4', 'Q5_Growth'],
    duplicates='drop'
)

# Calculate portfolio statistics
momentum_portfolios = analysis_df.groupby('momentum_quintile')['return_2024'].agg([
    'mean', 'std', 'count'
])
print("=== Momentum Portfolio Returns ===")
print(momentum_portfolios)

value_portfolios = analysis_df.groupby('value_quintile')['return_2024'].agg([
    'mean', 'std', 'count'
])
print("\n=== Value Portfolio Returns ===")
print(value_portfolios)

# %% [markdown]
# ## Story 1.7: Hypothesis Testing (20 mins)

# %%
print("=== Hypothesis Testing Framework (Statistical Inference) ===\n")

# Momentum hypothesis test
print("MOMENTUM FACTOR TEST:")
print("H0: μ(High Momentum) = μ(Low Momentum)")
print("H1: μ(High Momentum) > μ(Low Momentum)\n")

high_momentum = analysis_df[analysis_df['momentum_quintile'] == 'Q5_High']['return_2024']
low_momentum = analysis_df[analysis_df['momentum_quintile'] == 'Q1_Low']['return_2024']

# Perform t-test
t_stat_mom, p_value_mom = stats.ttest_ind(high_momentum, low_momentum, equal_var=False, nan_policy='omit')
print(f"T-statistic: {t_stat_mom:.4f}")
print(f"P-value: {p_value_mom:.4f}")
print(f"Mean difference: {high_momentum.mean() - low_momentum.mean():.4f}")
print(f"Conclusion: {'Reject H0' if p_value_mom < 0.05 else 'Fail to reject H0'}\n")

# Value hypothesis test
print("VALUE FACTOR TEST:")
print("H0: μ(Value stocks) = μ(Expensive stocks)")
print("H1: μ(Value stocks) > μ(Expensive stocks)\n")

value_stocks = analysis_df[analysis_df['value_quintile'] == 'Q1_Value']['return_2024']
expensive_stocks = analysis_df[analysis_df['value_quintile'] == 'Q5_Growth']['return_2024']

t_stat_val, p_value_val = stats.ttest_ind(value_stocks, expensive_stocks, equal_var=False, nan_policy='omit')
print(f"T-statistic: {t_stat_val:.4f}")
print(f"P-value: {p_value_val:.4f}")
print(f"Mean difference: {value_stocks.mean() - expensive_stocks.mean():.4f}")
print(f"Conclusion: {'Reject H0' if p_value_val < 0.05 else 'Fail to reject H0'}")

# %% [markdown]
# ## Story 1.8: Results Visualization (15 mins)

# %%
# Create comparison visualizations
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Momentum portfolios
momentum_means = momentum_portfolios['mean']
momentum_stds = momentum_portfolios['std'] / np.sqrt(momentum_portfolios['count'])
x_pos = np.arange(len(momentum_means))
axes[0].bar(x_pos, momentum_means, yerr=momentum_stds, capsize=5, alpha=0.7)
axes[0].set_xticks(x_pos)
axes[0].set_xticklabels(momentum_means.index, rotation=45)
axes[0].set_title('Mean Returns by Momentum Quintile')
axes[0].set_ylabel('Mean Return 2024')
axes[0].grid(True, alpha=0.3)

# Value portfolios
value_means = value_portfolios['mean']
value_stds = value_portfolios['std'] / np.sqrt(value_portfolios['count'])
x_pos = np.arange(len(value_means))
axes[1].bar(x_pos, value_means, yerr=value_stds, capsize=5, alpha=0.7)
axes[1].set_xticks(x_pos)
axes[1].set_xticklabels(value_means.index, rotation=45)
axes[1].set_title('Mean Returns by Value Quintile')
axes[1].set_ylabel('Mean Return 2024')
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# Calculate factor spreads
momentum_spread = momentum_means.iloc[-1] - momentum_means.iloc[0]
value_spread = value_means.iloc[0] - value_means.iloc[-1]

print(f"\n=== Factor Spreads ===")
print(f"Momentum Factor Spread (Q5-Q1): {momentum_spread:.4f}")
print(f"Value Factor Spread (Q1-Q5): {value_spread:.4f}")
print(f"Stronger Factor: {'Momentum' if abs(momentum_spread) > abs(value_spread) else 'Value'}")

# %% [markdown]
# ## Story 1.9: Final Conclusions (10 mins)

# %%
print("=== FINAL REPORT: Momentum vs Value Factor Performance ===\n")

print("1. DATA ANALYSIS:")
print(f"   - Analyzed {len(analysis_df)} stocks from Indian market")
print(f"   - Used proper data types and visualization techniques")
print(f"   - Identified patterns through EDA\n")

print("2. PROBABILITY MODELING:")
print(f"   - Modeled returns as random variables")
print(f"   - Expected return (mean): {returns.mean():.4f}")
print(f"   - Risk (std dev): {returns.std():.4f}")
if not np.isnan(p_value):
    print(f"   - Distribution is {'approximately normal' if p_value > 0.05 else 'non-normal'}\n")
else:
    print("   - Not enough data to formally test normality with Shapiro-Wilk\n")

print("3. STATISTICAL INFERENCE:")
print(f"   - Momentum factor spread: {momentum_spread:.4f}")
print(f"   - Value factor spread: {value_spread:.4f}")
print(f"   - Statistical significance:")
print(f"     * Momentum: {'Significant' if p_value_mom < 0.05 else 'Not significant'} (p={p_value_mom:.4f})")
print(f"     * Value: {'Significant' if p_value_val < 0.05 else 'Not significant'} (p={p_value_val:.4f})\n")

print("4. CONCLUSION:")
if abs(momentum_spread) > abs(value_spread):
    print("   Momentum factor showed stronger performance in 2024")
else:
    print("   Value factor showed stronger performance in 2024")

print("\n5. LIMITATIONS:")
print("   - Single year analysis (2024 only)")
print("   - Limited to Indian market")
print("   - Sample size constraints")
print("   - Survivorship bias possible")

print("\n6. FUTURE RESEARCH:")
print("   - Multi-year analysis")
print("   - Cross-market comparison")
print("   - Additional factors (Quality, Low Volatility)")
print("   - Risk-adjusted returns analysis")