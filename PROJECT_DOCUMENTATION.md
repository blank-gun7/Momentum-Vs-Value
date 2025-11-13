# Momentum vs Value Factor Performance Analysis
## A Statistical Investigation of Stock Market Returns in India (2024)

---

## Table of Contents
1. [Executive Summary](#executive-summary)
2. [Problem Statement](#problem-statement)
3. [Why This Matters: The Pain Point](#why-this-matters-the-pain-point)
4. [Theoretical Background](#theoretical-background)
5. [Methodology & Course Alignment](#methodology--course-alignment)
6. [Analysis Performed](#analysis-performed)
7. [Results & Findings](#results--findings)
8. [Statistical Interpretation](#statistical-interpretation)
9. [Conclusions & Recommendations](#conclusions--recommendations)
10. [Limitations & Future Work](#limitations--future-work)

---

## Executive Summary

This project investigates a fundamental question in investment management: **Which factor-based strategy delivers better returns - Momentum or Value?** Using statistical methods learned in Data Sciences coursework (Lectures 1-28), we analyze 122 Indian stocks to determine which investment philosophy performed better in 2024.

**Key Finding:** [PLACEHOLDER: Will be filled after analysis - either "Momentum factor showed superior performance with X% spread" or "Value factor dominated with Y% spread"]

---

## Problem Statement

### The Core Question
In equity investing, two competing philosophies have dominated academic and practical discourse:

1. **Momentum Investing**: The belief that stocks that have performed well recently will continue to perform well (winners keep winning)
2. **Value Investing**: The belief that undervalued stocks (low P/E ratios) will outperform overvalued ones (buy cheap, sell dear)

### Research Objective
Using Indian stock market data from 2023-2024, we aim to:
- Determine which factor (Momentum or Value) better explains stock returns in 2024
- Apply statistical methods to validate the significance of our findings
- Provide actionable insights for investment decision-making

### Specific Research Questions
1. Do high-momentum stocks (2023 winners) continue to outperform in 2024?
2. Do value stocks (low P/E) generate superior returns compared to growth stocks (high P/E)?
3. Which factor shows stronger statistical significance and larger economic impact?

---

## Why This Matters: The Pain Point

### 1. The Investor's Dilemma
Individual and institutional investors face a critical decision: **How should they select stocks for their portfolio?**

- **Without systematic analysis**, investors resort to:
  - Gut feelings and hunches
  - Following market rumors
  - Chasing past performance blindly
  - Making emotional decisions

- **The cost of wrong decisions**:
  - Underperformance vs market indices
  - Missed opportunities
  - Excessive portfolio turnover
  - Higher transaction costs

### 2. The Academic-Practice Gap
While academic finance has extensively studied factor investing, there's limited research on:
- **Emerging markets** like India
- **Recent time periods** (post-COVID market dynamics)
- **Simplified approaches** accessible to retail investors

### 3. Real-World Impact
This analysis addresses pain points for:

**Retail Investors:**
- Need evidence-based strategies
- Lack resources for complex analysis
- Require simple, actionable insights

**Portfolio Managers:**
- Need to justify investment decisions
- Require market-specific evidence
- Must explain strategy to clients

**Financial Advisors:**
- Need data to support recommendations
- Require simple explanations for clients
- Must understand factor performance

### 4. Economic Significance
The Indian equity market represents:
- **$4+ trillion market capitalization**
- **90+ million retail investors**
- **Growing institutional participation**

Even a 1% improvement in returns through better factor selection represents billions in value creation.

---

## Theoretical Background

### Momentum Factor
**Theory:** Behavioral finance suggests investors under-react to news, causing price trends to persist.

**Mechanism:**
- Initial under-reaction → gradual price adjustment → momentum
- Herding behavior amplifies trends
- Self-fulfilling prophecies

**Expected Pattern:** Stocks with high returns in period t should have high returns in period t+1

### Value Factor
**Theory:** Market inefficiencies cause some stocks to trade below intrinsic value.

**Mechanism:**
- Mean reversion in valuations
- Market overreaction to bad news
- Patient capital exploits mispricing

**Expected Pattern:** Low P/E stocks should outperform high P/E stocks

---

## Methodology & Statistical Framework

### Statistical Methods Integration

| Method Category | Core Topics | Application in Project |
|--------------|----------|----------------------|
| **Data Analysis** | Organization & Visualization | Data cleaning, descriptive statistics, visual exploration |
| **Probability Theory** | Distributions & Random Variables | Modeling returns, distribution analysis, risk metrics |
| **Statistical Inference** | Hypothesis Testing | Significance testing, confidence intervals, p-values |

### Analysis Framework

```
Raw Data (2023-2024)
    ↓
Data Cleaning & Integration → [Data Management & Organization]
    ↓
Factor Calculation
    ├── Momentum = (Price_end - Price_start)/Price_start
    └── Value = P/E Ratio ranking
    ↓
Exploratory Analysis → [Visualization & Descriptive Statistics]
    ↓
Probability Modeling → [Distribution Analysis]
    ↓
Portfolio Construction (Quintiles)
    ↓
Hypothesis Testing → [Statistical Inference]
    ↓
Conclusions
```

---

## Analysis Performed

### 1. Data Preparation & Cleaning
**Objective:** Create a clean, integrated dataset for analysis

**Steps Taken:**
- Loaded 453,672 price observations (2015-2024)
- Filtered to 92,589 observations (2023-2024)
- Merged with 5,910 fundamental data points
- Identified 122 common stocks with complete data
- Handled missing values and outliers

**Key Decisions:**
- Excluded stocks with negative P/E (not meaningful for value analysis)
- Required minimum 100 trading days for momentum calculation
- Removed extreme outliers (P/E > 100)

### 2. Exploratory Data Analysis

**Descriptive Statistics Computed:**
| Metric | Momentum 2023 | P/E Ratio 2023 | Returns 2024 |
|--------|--------------|----------------|--------------|
| Mean | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] |
| Median | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] |
| Std Dev | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] |
| Min | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] |
| Max | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] |

**Visualizations Created:**
- Histograms: Distribution shape analysis
- Scatter plots: Factor vs return relationships
- Correlation matrix: Inter-variable relationships
- Box plots: Outlier identification

**Key Observations:**
- [PLACEHOLDER: Distribution characteristics]
- [PLACEHOLDER: Correlation findings]
- [PLACEHOLDER: Outlier analysis]

### 3. Probability Modeling

**Returns as Random Variables:**
- Treated 2024 returns as realizations of random variable R
- Estimated parameters:
  - E[R] = [PLACEHOLDER]% (expected return)
  - Var(R) = [PLACEHOLDER] (variance)
  - σ(R) = [PLACEHOLDER]% (standard deviation/risk)

**Distribution Analysis:**
- Normality tests performed:
  - Shapiro-Wilk: p-value = [PLACEHOLDER]
  - Anderson-Darling: statistic = [PLACEHOLDER]
- Skewness: [PLACEHOLDER] (interpretation: [right/left]-skewed)
- Kurtosis: [PLACEHOLDER] (interpretation: [heavy/light]-tailed)

### 4. Portfolio Construction

**Quintile Formation:**
- Sorted 122 stocks into 5 groups (~24 stocks each)
- Momentum: Q1 (lowest) to Q5 (highest)
- Value: Q1 (lowest P/E = value) to Q5 (highest P/E = growth)

**Portfolio Performance:**

| Momentum Quintile | Mean Return | Std Dev | Sharpe-like Ratio |
|------------------|-------------|---------|-------------------|
| Q1 (Low) | [PLACEHOLDER]% | [PLACEHOLDER]% | [PLACEHOLDER] |
| Q2 | [PLACEHOLDER]% | [PLACEHOLDER]% | [PLACEHOLDER] |
| Q3 | [PLACEHOLDER]% | [PLACEHOLDER]% | [PLACEHOLDER] |
| Q4 | [PLACEHOLDER]% | [PLACEHOLDER]% | [PLACEHOLDER] |
| Q5 (High) | [PLACEHOLDER]% | [PLACEHOLDER]% | [PLACEHOLDER] |

| Value Quintile | Mean Return | Std Dev | Sharpe-like Ratio |
|---------------|-------------|---------|-------------------|
| Q1 (Value) | [PLACEHOLDER]% | [PLACEHOLDER]% | [PLACEHOLDER] |
| Q2 | [PLACEHOLDER]% | [PLACEHOLDER]% | [PLACEHOLDER] |
| Q3 | [PLACEHOLDER]% | [PLACEHOLDER]% | [PLACEHOLDER] |
| Q4 | [PLACEHOLDER]% | [PLACEHOLDER]% | [PLACEHOLDER] |
| Q5 (Growth) | [PLACEHOLDER]% | [PLACEHOLDER]% | [PLACEHOLDER] |

### 5. Hypothesis Testing

**Momentum Factor Test:**
- H₀: μ(High Momentum) = μ(Low Momentum)
- H₁: μ(High Momentum) ≠ μ(Low Momentum)
- Test statistic: t = [PLACEHOLDER]
- P-value: [PLACEHOLDER]
- Spread (Q5-Q1): [PLACEHOLDER]%
- 95% CI: [[PLACEHOLDER], [PLACEHOLDER]]

**Value Factor Test:**
- H₀: μ(Value stocks) = μ(Growth stocks)
- H₁: μ(Value stocks) ≠ μ(Growth stocks)
- Test statistic: t = [PLACEHOLDER]
- P-value: [PLACEHOLDER]
- Spread (Q1-Q5): [PLACEHOLDER]%
- 95% CI: [[PLACEHOLDER], [PLACEHOLDER]]

---

## Results & Findings

### Primary Finding
[PLACEHOLDER: Which factor performed better and by how much]

### Statistical Significance
- **Momentum:** [PLACEHOLDER: Significant/Not significant] at 5% level
- **Value:** [PLACEHOLDER: Significant/Not significant] at 5% level

### Economic Significance
- **Momentum spread:** [PLACEHOLDER]% annualized return difference
- **Value spread:** [PLACEHOLDER]% annualized return difference
- **Practical impact:** An investor following the [PLACEHOLDER: winning strategy] would have earned [PLACEHOLDER]% more than the opposite strategy

### Risk-Adjusted Performance
[PLACEHOLDER: Which strategy had better risk-adjusted returns based on Sharpe-like ratios]

---

## Statistical Interpretation

### What the Results Mean

**If Momentum is Significant (p < 0.05):**
- There is strong statistical evidence that past performance predicts future returns
- The probability of observing this pattern by chance is less than 5%
- Behavioral theories of under-reaction appear valid in Indian markets

**If Value is Significant (p < 0.05):**
- Statistical evidence supports the value premium in Indian markets
- Cheap stocks (low P/E) systematically outperform expensive ones
- Market inefficiencies can be exploited through value investing

**If Neither is Significant:**
- No strong evidence for either factor in the 2024 period
- Random chance could explain observed differences
- Other factors may be more important

### Confidence Intervals
The 95% confidence interval tells us:
- We are 95% confident the true factor spread lies within [PLACEHOLDER] to [PLACEHOLDER]%
- If we repeated this study many times, 95% of intervals would contain the true value

---

## Conclusions & Recommendations

### For Retail Investors
[PLACEHOLDER: Based on which factor wins]
1. **If Momentum wins:** Consider trend-following strategies, but beware of reversals
2. **If Value wins:** Focus on fundamental analysis and P/E ratios
3. **Risk management:** Diversify across both factors to reduce risk

### For Portfolio Managers
[PLACEHOLDER: Strategic recommendations based on findings]
- Factor allocation suggestions
- Timing considerations
- Risk management implications

### For Further Research
Key questions raised:
1. Why did [PLACEHOLDER: winning factor] outperform in 2024?
2. Is this pattern consistent across market cycles?
3. How do other factors (Quality, Size, Volatility) compare?

---

## Limitations & Future Work

### Current Study Limitations

1. **Temporal Limitation**
   - Single year analysis (2024)
   - May not represent long-term patterns
   - Specific to post-COVID market dynamics

2. **Sample Limitations**
   - 122 stocks (subset of total market)
   - Survivorship bias (excluded delisted stocks)
   - Limited to stocks with complete data

3. **Methodological Limitations**
   - Simple momentum definition (1-year returns)
   - P/E as sole value metric (ignores P/B, EV/EBITDA)
   - No risk adjustment beyond standard deviation

4. **Practical Limitations**
   - Ignores transaction costs
   - Assumes perfect execution
   - No consideration of taxes

### Recommended Extensions

1. **Temporal Extension**
   - Multi-year analysis (2020-2024)
   - Business cycle considerations
   - Rolling window analysis

2. **Factor Enhancement**
   - Composite value scores
   - Risk-adjusted momentum
   - Multi-factor models

3. **Practical Implementation**
   - Transaction cost analysis
   - Portfolio optimization
   - Real-time strategy testing

4. **Cross-Market Analysis**
   - Compare India vs developed markets
   - Sector-specific analysis
   - Small vs large cap differences

---

## Appendix: Statistical Concepts Applied

### Data Analysis Methods
✅ Variable types: Numerical (returns, P/E), Categorical (quintiles)
✅ Data cleaning: Missing value handling, outlier treatment
✅ Visualization: Histograms, scatter plots, box plots
✅ Descriptive statistics: Mean, median, standard deviation
✅ Correlation analysis: Factor relationships

### Probability Theory Applications
✅ Random variables: Returns modeled as R
✅ Probability distributions: Empirical vs theoretical
✅ Expected value: E[R] calculation
✅ Variance: Risk measurement
✅ Distribution testing: Normality assessment

### Statistical Inference Techniques
✅ Sampling: Stock universe as sample from population
✅ Point estimation: Sample means as estimates
✅ Hypothesis testing: Two-sample t-tests
✅ Confidence intervals: Uncertainty quantification
✅ Statistical significance: P-value interpretation

---

*Document prepared for Data Sciences Course Assignment*
*Analysis Period: 2023-2024 | Indian Stock Market*
*Total Stocks Analyzed: 122*