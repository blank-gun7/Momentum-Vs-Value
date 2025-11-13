import pandas as pd
import numpy as np
from scipy import stats

print("=" * 60)
print("EXPLORING: Fundamentals-Only Approach")
print("=" * 60)
print()

# ------------------------------------------------------------
# 1. LOAD DATA
# ------------------------------------------------------------
fundamentals_path = "Datasets/FUNDAMENTALratios.csv"  # change if needed
fundamentals = pd.read_csv(fundamentals_path)

print("1. DATASET OVERVIEW")
print(f"Shape: {fundamentals.shape}")
print(f"Columns: {fundamentals.columns.tolist()}")
print()

# ------------------------------------------------------------
# 2. CHECK WHAT PRICE DATA IS AVAILABLE INSIDE FUNDAMENTALS
# ------------------------------------------------------------
print("2. PRICE DATA AVAILABLE IN FUNDAMENTALS:")

price_like_cols = ["previousClose", "open", "dayLow", "dayHigh", "volume"]
for c in price_like_cols:
    if c in fundamentals.columns:
        print(f"  ✅ {c}")
    else:
        print(f"  ❌ {c} (not found)")
print()

# ------------------------------------------------------------
# 3. CHECK FUNDAMENTAL METRICS
# ------------------------------------------------------------
print("3. FUNDAMENTAL METRICS AVAILABLE:")

fundamental_cols = [
    "trailingPE",
    "earningsQuarterlyGrowth",
    "revenueGrowth",
    "debtToEquity",
    "pegRatio",
    "revenuePerShare",
]
for c in fundamental_cols:
    if c in fundamentals.columns:
        print(f"  ✅ {c}")
    else:
        print(f"  ❌ {c} (not found)")
print()

# ------------------------------------------------------------
# 4. BASIC DATA COMPLETENESS
# ------------------------------------------------------------
print("4. DATA COMPLETENESS CHECK:")

# Clean symbol: upper + strip spaces
fundamentals["stock_clean"] = (
    fundamentals["symbol"].astype(str).str.upper().str.strip()
)

unique_stocks = fundamentals["stock_clean"].nunique()
counts_per_stock = fundamentals["stock_clean"].value_counts()
multi_entry_stocks = (counts_per_stock > 1).sum()

print(f"Unique stocks (after cleaning): {unique_stocks}")
print(f"Stocks with multiple entries: {multi_entry_stocks}")
print()

# ------------------------------------------------------------
# 5. DATA QUALITY CHECK
# ------------------------------------------------------------
print("5. DATA QUALITY CHECK:")

prev_close_non_null = fundamentals["previousClose"].notna().sum() if "previousClose" in fundamentals.columns else 0
trailingPE_non_null = fundamentals["trailingPE"].notna().sum() if "trailingPE" in fundamentals.columns else 0

positive_pe = 0
if "trailingPE" in fundamentals.columns:
    pe_numeric = pd.to_numeric(fundamentals["trailingPE"], errors="coerce")
    positive_pe = (pe_numeric > 0).sum()

print(f"Non-null previousClose: {prev_close_non_null}/{len(fundamentals)}")
print(f"Non-null trailingPE: {trailingPE_non_null}/{len(fundamentals)}")
print(f"Positive P/E ratios: {positive_pe}")
print()

# ------------------------------------------------------------
# 6. MOMENTUM FEASIBILITY
# ------------------------------------------------------------
print("6. MOMENTUM CALCULATION FEASIBILITY:")
print("⚠️  ISSUE: We only have ONE day's price (previousClose, open, etc.)")
print("    - Cannot calculate 2023 annual momentum (need start/end prices)")
print("    - Cannot calculate 2024 returns (need time series)")
print()
print("7. POTENTIAL SOLUTIONS:")
print("Option A: Use earningsQuarterlyGrowth as momentum proxy")
print("Option B: Use revenueGrowth as momentum proxy")
print("Option C: Combine with stock price dataset for historical data")
print("Option D: Use price volatility (dayHigh - dayLow) as a factor")
print()

print("8. SIMPLIFIED ANALYSIS POSSIBLE:")
print("✅ Can still do value analysis (P/E ratios)")
print("✅ Can analyze growth metrics (earnings/revenue growth)")
print("✅ Can do cross-sectional analysis (single point in time)")
print("❌ Cannot do time-series momentum without historical prices")
print()

# ------------------------------------------------------------
# 9. SAMPLE ANALYSIS WITH FUNDAMENTALS ONLY
# ------------------------------------------------------------
print("9. SAMPLE ANALYSIS WITH FUNDAMENTALS ONLY:")

# Keep only rows where we have at least symbol, trailingPE, earningsQuarterlyGrowth, previousClose
required_cols = ["stock_clean", "trailingPE", "earningsQuarterlyGrowth", "previousClose"]
missing_required = [c for c in required_cols if c not in fundamentals.columns]
if missing_required:
    raise ValueError(f"Missing required columns in fundamentals: {missing_required}")

# Make an explicit copy to avoid SettingWithCopyWarning
fundamentals_clean = fundamentals[required_cols].copy()

# Convert to numeric safely
fundamentals_clean["pe_ratio"] = pd.to_numeric(
    fundamentals_clean["trailingPE"], errors="coerce"
)
fundamentals_clean["earnings_growth"] = pd.to_numeric(
    fundamentals_clean["earningsQuarterlyGrowth"], errors="coerce"
)
fundamentals_clean["previousClose"] = pd.to_numeric(
    fundamentals_clean["previousClose"], errors="coerce"
)

# Drop rows missing key fields and require positive P/E
fundamentals_clean = fundamentals_clean.dropna(subset=["pe_ratio", "earnings_growth", "previousClose"])
fundamentals_clean = fundamentals_clean[fundamentals_clean["pe_ratio"] > 0]

print(f"\nStocks with valid P/E and earnings growth: {len(fundamentals_clean)}\n")

print("Sample data:")
print(
    fundamentals_clean[
        ["stock_clean", "pe_ratio", "earnings_growth", "previousClose"]
    ].head()
)
print()

# Correlation between P/E and earnings growth
corr_matrix = fundamentals_clean[["pe_ratio", "earnings_growth"]].corr()
print("Correlation between P/E and Earnings Growth:")
print(corr_matrix)
print()

print("=" * 60)
print("RECOMMENDATION:")
print("=" * 60)
print()
print("PROS of Fundamentals-Only:")
print("✅ Simpler - one dataset")
print("✅ All metrics in one place")
print("✅ No merging required")
print("✅ Good for value analysis")
print()
print("CONS of Fundamentals-Only:")
print("❌ No historical prices for momentum calculation")
print("❌ Can't calculate annual returns (2023 → 2024)")
print("❌ Limited to snapshot analysis")
print("❌ Loses time-series dimension")
print()
print("VERDICT: Keep the two-dataset approach for full momentum vs value analysis")
print("         OR modify the analysis to focus on growth vs value instead")
print()