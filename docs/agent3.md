# AI-Powered Tax Optimization Engine

A sophisticated Python-based tax planning platform that combines federal tax calculations, portfolio analysis, and AI-driven strategies to minimize tax liability and maximize wealth accumulation. Designed for individual investors, financial advisors, and tax professionals.

## 🎯 Key Features

- **Real-Time Tax Calculation**: Accurate federal income tax, capital gains tax, and Net Investment Income Tax (NIIT) computations
- **Tax Loss Harvesting**: Identifies unrealized losses to offset gains and ordinary income
- **Roth Conversion Analysis**: Optimizes IRA to Roth conversions based on age, income, and tax brackets
- **Charitable Giving Strategy**: Recommends optimal assets for tax-efficient donations
- **Retirement Contribution Planning**: Maximizes tax-advantaged account contributions
- **Portfolio Integration**: Real-time price updates via Yahoo Finance
- **2024 Tax Brackets**: Current federal tax rates and capital gains thresholds
- **Wash Sale Avoidance**: Suggests replacement securities to avoid wash sale violations
- **AI-Powered Insights**: GPT-powered strategic analysis and recommendations
- **Comprehensive Reporting**: Detailed tax optimization reports with actionable strategies

## 📋 Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [Architecture](#architecture)
- [API Reference](#api-reference)
- [Tax Strategies](#tax-strategies)
- [Configuration](#configuration)
- [Examples](#examples)

## 🚀 Installation

### Prerequisites

- Python 3.8+
- OpenAI API key (for AI insights)
- Yahoo Finance account (free data)

### Dependencies

```bash
pip install openai pandas numpy scipy yfinance python-dotenv
```

### Setup

1. Clone or download the repository

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
export OPENAI_API="your_openai_api_key"
```

Or create a `.env` file:
```
OPENAI_API=your_openai_api_key
```

## 🎯 Quick Start

### Basic Usage

```python
from tax_optimization import (
    TaxOptimizationEngine,
    PortfolioManager,
    TaxProfile,
    TaxFilingStatus,
    create_sample_portfolio
)

# Create tax profile
profile = TaxProfile(
    filing_status=TaxFilingStatus.MARRIED_JOINT,
    annual_income=180000,
    state="CA",
    age=42
)

# Create portfolio
positions = create_sample_portfolio()
portfolio = PortfolioManager(positions)

# Run optimization
engine = TaxOptimizationEngine(portfolio, profile)
optimizations = engine.run_complete_analysis()

# View results
for opt in optimizations:
    print(f"{opt.strategy.value}: ${opt.estimated_tax_savings:,.0f} savings")
```

### Interactive Mode

```python
from tax_optimization import interactive_mode

# Launch guided interview
report = interactive_mode()
```

## 📖 Usage

### Complete Analysis Pipeline

```python
from tax_optimization import TaxOptimizationEngine, PortfolioManager, TaxProfile, TaxReportGenerator
import json

# 1. Define tax profile
profile = TaxProfile(
    filing_status=TaxFilingStatus.SINGLE,
    annual_income=150000,
    state="NY",
    age=35,
    traditional_401k_contributions=10000,
    short_term_gains=5000,
    long_term_gains=15000
)

# 2. Create portfolio with positions
portfolio = PortfolioManager(positions)

# 3. Initialize optimization engine
engine = TaxOptimizationEngine(portfolio, profile)

# 4. Run complete analysis
optimizations = engine.run_complete_analysis()

# 5. Generate report
report_gen = TaxReportGenerator()
report = report_gen.generate_report(engine)
print(report)
```

### Component-Based Usage

```python
from tax_optimization import FederalTaxCalculator

# Calculate taxes independently
calculator = FederalTaxCalculator()
tax_calc = calculator.calculate_total_tax(profile)

print(f"AGI: ${tax_calc['agi']:,.0f}")
print(f"Taxable Income: ${tax_calc['taxable_income']:,.0f}")
print(f"Total Federal Tax: ${tax_calc['total_federal_tax']:,.0f}")
print(f"Effective Rate: {tax_calc['effective_rate']:.2%}")
```

### Tax Loss Harvesting

```python
# Find and execute tax loss harvesting
loss_opportunities = engine.analyze_tax_loss_harvesting()

for opportunity in loss_opportunities:
    print(f"Description: {opportunity.description}")
    print(f"Estimated Savings: ${opportunity.estimated_tax_savings:,.0f}")
    print("Positions to Sell:")
    for pos in opportunity.positions_to_sell:
        print(f"  - {pos.ticker}: {pos.quantity} shares")
    print("Suggested Replacements:")
    for replacement in opportunity.positions_to_buy:
        print(f"  - {replacement}")
```

## 🏗️ Architecture

### System Overview

```
User Input (Profile, Portfolio)
    ↓
Tax Profile Manager → TaxProfile (filing status, income, contributions)
    ↓
Portfolio Manager → Update prices via yfinance
    ↓
Tax Optimization Engine
    ├── Tax Loss Harvesting Analysis
    ├── Roth Conversion Analysis
    ├── Charitable Giving Strategy
    └── Retirement Contribution Analysis
    ↓
Federal Tax Calculator → Compute tax liability
    ↓
LLM Analysis (GPT) → Generate strategic insights
    ↓
Report Generator → Comprehensive tax optimization report
```

### Agent Components

1. **FederalTaxCalculator**: Computes federal income tax and capital gains tax
2. **PortfolioManager**: Manages positions and fetches real-time prices
3. **TaxOptimizationEngine**: Orchestrates all optimization strategies
4. **TaxReportGenerator**: Generates formatted reports
5. **LLM Insights Generator**: AI-powered strategic recommendations

## 📚 API Reference

### Core Classes

#### `TaxProfile`

Represents a taxpayer's complete tax situation.

**Constructor Parameters:**
- `filing_status`: TaxFilingStatus enum
- `annual_income`: float - W-2 or self-employment income
- `state`: str - Two-letter state code
- `age`: int - Age for retirement account limits
- `standard_deduction`: float (auto-calculated if 0)
- `itemized_deductions`: float
- `traditional_401k_contributions`: float
- `roth_401k_contributions`: float
- `traditional_ira_contributions`: float
- `roth_ira_contributions`: float
- `hsa_contributions`: float
- `short_term_gains`: float - Realized capital gains
- `long_term_gains`: float - Realized capital gains
- `carryforward_losses`: float - Prior year loss carryforward

**Methods:**
- `copy()`: Create a copy for scenario analysis

#### `Position`

Represents a single investment position.

**Constructor Parameters:**
- `ticker`: str - Stock symbol
- `quantity`: float - Number of shares
- `purchase_price`: float - Cost per share
- `purchase_date`: datetime - Date acquired
- `current_price`: float - Current market price
- `account_type`: AccountType enum
- `asset_class`: AssetClass enum

**Methods:**
- `get_cost_basis()`: Total purchase cost
- `get_market_value()`: Current market value
- `get_unrealized_gain_loss()`: Profit/loss amount
- `get_holding_period_days()`: Days held
- `is_long_term()`: Boolean (held > 365 days)

#### `PortfolioManager`

Manages multiple positions and portfolio statistics.

**Constructor:**
```python
portfolio = PortfolioManager(positions: List[Position])
```

**Methods:**
- `update_prices()`: Fetch current prices from Yahoo Finance
- `get_taxable_positions()`: Positions in taxable accounts
- `get_unrealized_losses()`: Loss positions available for harvesting
- `get_unrealized_gains()`: Gain positions
- `get_portfolio_summary()`: Dict with portfolio statistics

#### `FederalTaxCalculator`

Calculates federal income and capital gains tax.

**Methods:**
- `calculate_ordinary_income_tax(taxable_income, filing_status)`: float
- `calculate_ltcg_tax(ltcg, taxable_income, filing_status)`: float
- `calculate_total_tax(profile)`: Dict with detailed breakdown

**Tax Calculation Returns:**
```python
{
    "agi": float,
    "taxable_income": float,
    "ordinary_tax": float,
    "stcg_tax": float,
    "ltcg_tax": float,
    "niit": float,
    "total_federal_tax": float,
    "effective_rate": float
}
```

#### `TaxOptimization`

Represents a tax optimization recommendation.

**Fields:**
- `strategy`: TaxStrategy enum
- `description`: str - Human-readable description
- `estimated_tax_savings`: float
- `action_items`: List[str] - Steps to implement
- `priority`: int (1-5, lower is higher priority)
- `deadline`: Optional[datetime]
- `positions_to_sell`: List[Position]
- `positions_to_buy`: List[str] - Ticker symbols
- `amount`: float - Dollar amount involved

#### `TaxOptimizationEngine`

Main orchestration engine for tax optimization.

**Constructor:**
```python
engine = TaxOptimizationEngine(
    portfolio: PortfolioManager,
    tax_profile: TaxProfile
)
```

**Methods:**
- `analyze_tax_loss_harvesting()`: List[TaxOptimization]
- `analyze_roth_conversion()`: List[TaxOptimization]
- `analyze_charitable_giving()`: List[TaxOptimization]
- `analyze_retirement_contributions()`: List[TaxOptimization]
- `run_complete_analysis()`: List[TaxOptimization] - Runs all strategies

#### `TaxReportGenerator`

Generates comprehensive tax optimization reports.

**Methods:**
- `generate_report(engine: TaxOptimizationEngine)`: str - Markdown report

### Enumerations

#### `TaxFilingStatus`
- `SINGLE`
- `MARRIED_JOINT`
- `MARRIED_SEPARATE`
- `HEAD_OF_HOUSEHOLD`

#### `TaxStrategy`
- `TAX_LOSS_HARVEST`: Harvest losses to offset gains
- `ROTH_CONVERSION`: Convert Traditional IRA to Roth
- `CHARITABLE_DONATION`: Donate appreciated securities
- `CAPITAL_GAIN_TIMING`: Time realization of gains
- `RETIREMENT_CONTRIBUTION`: Maximize retirement savings

#### `AccountType`
- `TAXABLE`: Standard brokerage account
- `TRADITIONAL_IRA`: Pre-tax retirement account
- `ROTH_IRA`: Post-tax retirement account
- `TRADITIONAL_401K`: Employer pre-tax plan
- `ROTH_401K`: Employer post-tax plan
- `HSA`: Health Savings Account

#### `AssetClass`
- `EQUITY`: Stocks and ETFs
- `BOND`: Fixed income securities
- `REAL_ESTATE`: Real estate investments
- `CRYPTO`: Cryptocurrency
- `CASH`: Cash equivalents

## 🧮 Tax Strategies Explained

### Tax Loss Harvesting

Identifies positions with unrealized losses and recommends selling them to offset capital gains and up to $3,000 of ordinary income annually.

**When to Use:**
- Have unrealized losses in taxable account
- Want to offset capital gains
- Need to reduce ordinary income

**Benefits:**
- Immediate tax deduction
- Can reinvest in similar assets
- Harvest up to $3,000/year in ordinary income

**Considerations:**
- Wash sale rules (30-day window)
- Replacement securities provided automatically
- Long-term vs. short-term loss treatment

### Roth Conversion

Converts funds from Traditional IRA to Roth IRA, paying taxes now for tax-free growth later.

**When to Use:**
- In low-income years
- Before Required Minimum Distributions begin
- Expect higher tax rates in retirement
- Age < 59.5 (no early withdrawal penalty on conversions)

**Benefits:**
- Tax-free growth on converted amounts
- Tax-free withdrawals in retirement
- No RMDs during your lifetime

**Considerations:**
- Pro-rata rule (affects all Traditional IRAs)
- Conversion creates immediate tax liability
- May trigger IRMAA increases for Medicare

### Charitable Donation

Recommends donating appreciated long-term positions instead of cash.

**When to Use:**
- Have highly appreciated long-term securities
- Planning to make charitable contributions
- Itemizing deductions

**Benefits:**
- Avoid capital gains tax on appreciation
- Full fair market value as deduction
- Potentially higher deduction value

**Considerations:**
- Must use appreciated securities (not cash)
- Requires appraisal if > $5,000
- Must donate to qualified charity

### Retirement Contributions

Identifies remaining contribution room for tax-advantaged accounts.

**When to Use:**
- Have contribution room available
- Want to reduce taxable income
- Planning for retirement

**Benefits:**
- Immediate tax deduction
- Tax-deferred or tax-free growth
- Reduced current year tax liability

**2024 Contribution Limits:**
- 401(k): $23,000 ($30,500 if 50+)
- IRA: $7,000 ($8,000 if 50+)
- HSA: $4,150 individual / $8,300 family

## ⚙️ Configuration

### 2024 Tax Brackets

Federal tax brackets are hard-coded for 2024 and can be updated annually:

```python
# In FederalTaxCalculator
BRACKETS_2024 = {
    TaxFilingStatus.SINGLE: [
        (11600, 0.10),
        (47150, 0.12),
        # ... additional brackets
    ]
}
```

### Capital Gains Brackets

Long-term capital gains use preferential rates:

```python
LTCG_BRACKETS = {
    TaxFilingStatus.SINGLE: [
        (47025, 0.0),      # 0% rate
        (518900, 0.15),    # 15% rate
        (float('inf'), 0.20)  # 20% rate
    ]
}
```

### NIIT (Net Investment Income Tax)

3.8% tax on investment income when Modified AGI exceeds thresholds:
- Single: $200,000
- Married Joint: $250,000
- Modify in `calculate_total_tax()` method

## 💡 Examples

### Example 1: Complete Tax Analysis

```python
from tax_optimization import *

# Create profile for married couple, CA resident
profile = TaxProfile(
    filing_status=TaxFilingStatus.MARRIED_JOINT,
    annual_income=250000,
    state="CA",
    age=45,
    traditional_401k_contributions=23000,
    short_term_gains=10000,
    long_term_gains=50000
)

# Create portfolio with positions
portfolio = PortfolioManager(create_sample_portfolio())

# Run analysis
engine = TaxOptimizationEngine(portfolio, profile)
optimizations = engine.run_complete_analysis()

# Display results
for opt in optimizations:
    print(f"Priority {opt.priority}: {opt.description}")
    print(f"  Savings: ${opt.estimated_tax_savings:,.0f}\n")
```

### Example 2: Tax Loss Harvesting

```python
# Find tax loss harvesting opportunities
harvesting = engine.analyze_tax_loss_harvesting()

if harvesting:
    strategy = harvesting[0]
    print(f"Harvest ${strategy.amount:,.0f} in losses")
    print("\nSell these positions:")
    for pos in strategy.positions_to_sell:
        print(f"  {pos.ticker}: {pos.quantity} shares @ ${pos.current_price}")
    print("\nBuy these replacements:")
    for replacement in strategy.positions_to_buy[:3]:
        print(f"  {replacement}")
```

### Example 3: Generate AI Insights

```python
# Get AI-powered strategic recommendations
insights = generate_ai_insights(engine, optimizations)
print(insights)
```

### Example 4: Custom Tax Scenario

```python
# Test impact of additional Roth conversion
test_profile = profile.copy()
test_profile.long_term_gains += 50000  # Simulate $50k conversion

calculator = FederalTaxCalculator()
baseline = calculator.calculate_total_tax(profile)
with_conversion = calculator.calculate_total_tax(test_profile)

print(f"Tax increase from conversion: ${with_conversion['total_federal_tax'] - baseline['total_federal_tax']:,.0f}")
```

## 📊 Report Output

The system generates comprehensive reports in Markdown format with:

- Taxpayer profile summary
- Current tax situation breakdown
- Portfolio analysis
- Tax optimization opportunities (prioritized)
- Detailed action items for each strategy
- Year-end tax checklist
- Legal disclaimers
- Next steps

### Sample Output Sections

```markdown
# TAX OPTIMIZATION REPORT

## CURRENT TAX SITUATION
- **Total Federal Tax**: $45,000
- **Effective Tax Rate**: 25%
- **Taxable Income**: $180,000

## OPTIMIZATION OPPORTUNITIES
1. 🔥 Tax Loss Harvesting: $8,500 savings
2. ⭐ Roth Conversion: $12,000 savings
3. 💡 Retirement Contributions: $5,500 savings

**Total Potential Savings**: $26,000
```

## 🔐 Security & Compliance

### Important Disclaimers

⚠️ **This tool provides informational analysis only and is not tax advice.**

- Consult a licensed tax professional before implementing strategies
- Tax laws vary by state and change annually
- Wash sale rules have specific timing requirements
- Individual circumstances significantly affect strategy suitability
- Results are based on provided information accuracy

### Best Practices

1. **Update positions regularly** via `portfolio.update_prices()`
2. **Verify tax brackets** annually for current year
3. **Document all transactions** for tax reporting
4. **Consult professionals** before implementation
5. **Monitor carry-forward losses** across years
6. **Track wash sale periods** (30-day window)

## 🐛 Troubleshooting

### Issue: "Invalid price data"
**Solution**: Check Yahoo Finance connectivity; verify ticker symbols are correct

### Issue: "Contribution limit calculations off"
**Solution**: Verify age-based catch-up eligibility; update limits for current year

### Issue: "Wash sale overlap detected"
**Solution**: Wait 31 days or buy replacement securities first

## 📈 Performance Notes

- Tax calculations: < 100ms
- Portfolio updates: 2-5 seconds per ticker
- Complete analysis: 5-10 seconds
- Report generation: < 1 second

## 🔄 Dependencies

- `openai` - GPT integration for AI insights
- `pandas` - Data manipulation
- `numpy` - Numerical computations
- `scipy` - Optimization algorithms
- `yfinance` - Real-time price data
- `python-dotenv` - Environment variable management

## 📝 License

[Add your license here]

## 🤝 Support & Contributing

For issues, questions, or feature requests, please contact your financial advisor or tax professional.

## 🚀 Future Enhancements

- State and local tax (SALT) optimization
- Alternative Minimum Tax (AMT) calculations
- Multi-state resident analysis
- Self-employment tax optimization
- Estimated quarterly tax planning
- Real brokerage API integration
- PDF report export
- Portfolio rebalancing tax impact
- Estate planning integration
- Cryptocurrency tax reporting

## 📚 Additional Resources

- [IRS Tax Information](https://www.irs.gov)
- [2024 Tax Brackets](https://www.irs.gov/newsroom/irs-provides-tax-inflation-adjustments-for-tax-year-2024)
- [Publication 550 - Investment Income and Expenses](https://www.irs.gov/publications/p550)
- [Form 8949 - Sales of Capital Assets](https://www.irs.gov/forms-pubs/form-8949)

---

*AI-Powered Tax Optimization Engine v1.0*  
*For informational purposes. Consult tax professional for advice.*