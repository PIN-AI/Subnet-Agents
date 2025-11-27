# Enterprise Financial Analysis System

A comprehensive Python-based financial analysis platform that combines real-time financial data, machine learning forecasting, risk assessment, and AI-driven insights to provide institutional-grade investment analysis and reporting.

## 🌟 Features

- **Real-Time Financial Data Fetching**: Retrieves current financial metrics, historical prices, and comprehensive statements from Yahoo Finance
- **Time Series Forecasting**: Uses Facebook Prophet for accurate cash flow and revenue predictions
- **Risk Assessment Engine**: Evaluates liquidity, market, debt, and overall portfolio risk with scoring
- **Market Intelligence**: Gathers real-time news and market analysis from multiple sources
- **Anomaly Detection**: Identifies unusual patterns in financial data using Isolation Forest
- **AI-Powered Analysis**: Leverages GPT to generate actionable insights and strategic recommendations
- **Structured JSON Reporting**: Generates comprehensive, machine-readable financial reports
- **Multi-Metric Analysis**: Analyzes revenue, free cash flow, net income, debt, and more

## 📋 Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [Architecture](#architecture)
- [API Reference](#api-reference)
- [Configuration](#configuration)
- [Output Format](#output-format)
- [Examples](#examples)

## 🚀 Installation

### Prerequisites

- Python 3.8+
- OpenAI API key
- SerpAPI key (for market intelligence)

### Dependencies

```bash
pip install openai requests pandas prophet numpy scikit-learn matplotlib yfinance python-dotenv
```

### Setup

1. Clone or download the repository

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
export OPENAI_API="your_openai_api_key"
export SERP_API_KEY="your_serpapi_key"
```

Or create a `.env` file:
```
OPENAI_API=your_openai_api_key
SERP_API_KEY=your_serpapi_key
```

## 🎯 Quick Start

### Basic Usage

```python
from financial_analysis import run_financial_analysis

# Run analysis with natural language query
report = run_financial_analysis("Analyze Apple stock for the next 6 months")

# Access specific report sections
company_info = report['company']
risk_data = report['risk_assessment']
forecasts = report['forecasts']
analysis = report['analysis']
```

### Query Examples

The system accepts natural language queries and automatically extracts parameters:

```python
# Comprehensive analysis
report = run_financial_analysis("I want comprehensive analysis of Microsoft for long-term investment")

# Tech sector analysis
report = run_financial_analysis("Analyze best electronics company stock for next 6 months")

# Fundamental analysis
report = run_financial_analysis("Fundamental analysis of Tesla stock")
```

## 📖 Usage

### Run Full Analysis Pipeline

```python
from financial_analysis import run_financial_analysis
import json

# Execute analysis
report = run_financial_analysis("Analyze AAPL stock")

# Output as formatted JSON
print(json.dumps(report, indent=2))

# Or save to file
with open('aapl_analysis.json', 'w') as f:
    json.dump(report, f, indent=2)
```

### Component-Based Usage

For more granular control:

```python
from financial_analysis import (
    FinancialDataAgent,
    MLAnalysisAgent,
    RiskAssessmentAgent,
    LLMAnalysisAgent
)

# Fetch data
data_agent = FinancialDataAgent()
financials = data_agent.fetch_company_data("AAPL", period="2y")

# Run ML forecasting
ml_agent = MLAnalysisAgent()
forecast = ml_agent.forecast_metric(
    data=metric_data,
    periods=4,
    metric_name="revenue"
)

# Assess risks
risk_agent = RiskAssessmentAgent()
risk_assessment = risk_agent.assess_risks(financials, forecasts)
```

## 🏗️ Architecture

### Agent-Based System

The system is built on a multi-agent architecture with specialized components:

```
User Query
    ↓
agent_understand() → Extract parameters (ticker, analysis type, horizon)
    ↓
FinancialDataAgent → Fetch real-time financial data from Yahoo Finance
    ↓
ResearchAgent → Gather market intelligence and news
    ↓
MLAnalysisAgent → Generate forecasts using Prophet
    ↓
RiskAssessmentAgent → Evaluate financial risks
    ↓
LLMAnalysisAgent → Generate AI-powered insights
    ↓
ReportingAgent → Compile JSON report
    ↓
Structured JSON Report
```

## 📚 API Reference

### Core Classes

#### `FinancialDataAgent`

Fetches and processes real financial data.

**Methods:**

- `fetch_company_data(ticker: str, period: str = "2y") -> CompanyFinancials`
  - Retrieves comprehensive financial data for a company
  - Returns: CompanyFinancials object with all metrics

- `extract_metric_series(financials: CompanyFinancials, metric: FinancialMetric) -> pd.DataFrame`
  - Extracts time series for a specific financial metric
  - Returns: DataFrame with 'ds' (date) and 'y' (value) columns

#### `CompanyFinancials`

Data class containing comprehensive company financial information.

**Fields:**
- `ticker`: Stock ticker symbol
- `company_name`: Full company name
- `sector`: Industry sector
- `market_cap`: Market capitalization
- `current_price`: Current stock price
- `pe_ratio`: Price-to-earnings ratio
- `debt_to_equity`: Debt-to-equity ratio
- `current_ratio`: Current ratio (liquidity measure)
- `volatility`: Annualized volatility
- `beta`: Stock beta coefficient
- `historical_prices`: DataFrame of historical prices
- `cash_flow_statement`: Cash flow data
- `income_statement`: Income statement data
- `balance_sheet`: Balance sheet data

#### `MLAnalysisAgent`

Performs time series forecasting and anomaly detection.

**Methods:**

- `forecast_metric(data: pd.DataFrame, periods: int, metric_name: str) -> ForecastResult`
  - Forecasts financial metrics using Prophet
  - **Parameters:**
    - `data`: DataFrame with 'ds' and 'y' columns
    - `periods`: Number of quarters to forecast
    - `metric_name`: Name of the metric being forecasted
  - **Returns:** ForecastResult with predictions and confidence intervals

#### `ForecastResult`

Contains forecasting results.

**Fields:**
- `metric_name`: Name of forecasted metric
- `predicted_values`: List of forecast values
- `confidence_lower`: Lower confidence interval
- `confidence_upper`: Upper confidence interval
- `trend_direction`: "increasing", "decreasing", or "stable"
- `growth_rate`: Percentage change projected

#### `RiskAssessmentAgent`

Evaluates comprehensive financial risk.

**Methods:**

- `assess_risks(financials: CompanyFinancials, forecast_results: Dict[str, ForecastResult]) -> RiskAssessment`
  - Evaluates liquidity, market, and debt risks
  - Returns: RiskAssessment object with risk scores and factors

#### `RiskAssessment`

Risk evaluation results.

**Fields:**
- `overall_risk`: RiskLevel (LOW, MODERATE, HIGH, CRITICAL)
- `liquidity_risk`: Liquidity assessment
- `market_risk`: Market volatility risk
- `debt_risk`: Leverage-related risk
- `risk_factors`: List of specific risk factors identified
- `risk_score`: Numerical risk score (0-1)

#### `ResearchAgent`

Fetches market intelligence and news.

**Methods:**

- `fetch_market_intelligence(company_name: str, analysis_type: AnalysisType) -> str`
  - Retrieves recent news and analysis
  - Returns: Formatted string with news snippets

#### `LLMAnalysisAgent`

Generates AI-powered financial analysis.

**Methods:**

- `generate_analysis(financials, forecasts, risk_assessment, market_intel) -> Dict`
  - Generates structured analysis with executive summary, cash flow analysis, risk evaluation, outlook, and recommendations
  - Returns: Dictionary with full_analysis and summary fields

#### `ReportingAgent`

Generates structured JSON reports.

**Methods:**

- `generate_json_report(financials, forecasts, risk_assessment, llm_analysis, market_intel) -> Dict`
  - Compiles all analyses into a comprehensive report
  - Returns: Complete JSON report with all data and insights

### Enumerations

#### `AnalysisType`
- `CASH_FLOW`: Focus on cash flow analysis
- `REVENUE`: Focus on revenue trends
- `RISK`: Focus on risk assessment
- `COMPREHENSIVE`: Full analysis

#### `RiskLevel`
- `LOW`: Low risk
- `MODERATE`: Moderate risk
- `HIGH`: High risk
- `CRITICAL`: Critical risk level

#### `TimeHorizon`
- `SHORT_TERM`: 30 days
- `MEDIUM_TERM`: 90 days
- `LONG_TERM`: 180 days
- `ANNUAL`: 365 days

#### `FinancialMetric`
- `FREE_CASH_FLOW`: Free cash flow
- `OPERATING_CASH_FLOW`: Operating cash flow
- `REVENUE`: Total revenue
- `NET_INCOME`: Net income
- `EBITDA`: EBITDA
- `TOTAL_DEBT`: Total debt
- `TOTAL_CASH`: Total cash

### Key Functions

#### `agent_understand(query: str) -> Dict`

Parses natural language query and extracts structured parameters.

**Parameters:**
- `query`: Natural language query string

**Returns:**
```json
{
  "ticker": "AAPL",
  "analysis_type": "comprehensive",
  "forecast_horizon": "long_term",
  "currency": "USD"
}
```

#### `run_financial_analysis(query: str) -> Dict`

Main entry point for complete financial analysis.

**Parameters:**
- `query`: Natural language query describing the analysis needed

**Returns:** Complete JSON report with all analyses

## ⚙️ Configuration

### Model Selection

The system uses GPT models for AI analysis. Configure in the code:

```python
MODEL_NAME = "gpt-4-turbo"  # Change to your preferred model
```

### Forecast Periods

Adjust the number of quarters to forecast:

```python
# In run_financial_analysis()
forecast = ml_agent.forecast_metric(
    metric_data,
    periods=8,  # Forecast 8 quarters instead of 4
    metric_name=metric_name
)
```

### Historical Data Period

Modify the lookback period for financial data:

```python
financials = data_agent.fetch_company_data(ticker, period="5y")  # 5 years instead of 2
```

### Prophet Model Parameters

Adjust forecasting model parameters:

```python
model = Prophet(
    yearly_seasonality=True,
    weekly_seasonality=False,
    daily_seasonality=False,
    changepoint_prior_scale=0.05  # Adjust sensitivity to trend changes
)
```

## 📊 Output Format

### Complete Report Structure

```json
{
  "metadata": {
    "report_date": "2025-01-15T10:30:00",
    "analysis_period": "Last 2 years + 6-month forecast",
    "generated_by": "Enterprise Financial Analysis System"
  },
  "company": {
    "ticker": "AAPL",
    "company_name": "Apple Inc.",
    "sector": "Technology",
    "market_cap": 3200000000000,
    "current_price": 195.50,
    "pe_ratio": 28.5,
    "debt_to_equity": 1.92,
    "volatility": 0.24,
    "beta": 1.2
  },
  "risk_assessment": {
    "overall_risk": "moderate",
    "liquidity_risk": "low",
    "market_risk": "moderate",
    "debt_risk": "moderate",
    "risk_factors": ["Moderate volatility: 24.00%"],
    "risk_score": 0.45
  },
  "forecasts": {
    "cash_flow": {
      "metric_name": "cash_flow",
      "trend_direction": "increasing",
      "growth_rate": 8.5,
      "predicted_values": [115000000, 118000000, 122000000, 125000000],
      "average_forecast": 120000000
    },
    "revenue": {
      "metric_name": "revenue",
      "trend_direction": "increasing",
      "growth_rate": 6.2,
      "predicted_values": [395000000, 402000000, 410000000, 418000000],
      "average_forecast": 406000000
    }
  },
  "market_intelligence": "Recent earnings beat expectations...",
  "analysis": {
    "full_analysis": "Executive Summary: Apple demonstrates strong financial health...",
    "summary": "Strong financial position with positive growth trajectory"
  },
  "disclaimer": "This report is for informational purposes only..."
}
```

## 💡 Examples

### Example 1: Tech Company Analysis

```python
from financial_analysis import run_financial_analysis
import json

report = run_financial_analysis("Analyze Microsoft for next 6 months")
print(json.dumps(report['company'], indent=2))
print(report['analysis']['full_analysis'])
```

### Example 2: Risk-Focused Analysis

```python
report = run_financial_analysis("What's the risk profile of Tesla stock?")
risk = report['risk_assessment']
print(f"Overall Risk: {risk['overall_risk']}")
print(f"Risk Score: {risk['risk_score']}")
for factor in risk['risk_factors']:
    print(f"  - {factor}")
```

### Example 3: Forecast Analysis

```python
report = run_financial_analysis("Forecast Amazon revenue for the next year")
revenue_forecast = report['forecasts'].get('revenue', {})
print(f"Trend: {revenue_forecast['trend_direction']}")
print(f"Growth Rate: {revenue_forecast['growth_rate']:.2f}%")
print(f"Average Forecast: ${revenue_forecast['average_forecast']:,.0f}")
```

## ⚠️ Risk Assessment Thresholds

| Metric | Low Risk | Moderate Risk | High Risk |
|--------|----------|---------------|-----------|
| Current Ratio | > 1.5 | 1.0 - 1.5 | < 1.0 |
| Volatility | < 25% | 25% - 40% | > 40% |
| Debt-to-Equity | < 1.0 | 1.0 - 2.0 | > 2.0 |
| Risk Score | < 0.3 | 0.3 - 0.7 | > 0.7 |

## 🔐 Security Notes

- **API Keys**: Never hardcode API keys in production. Use environment variables
- **Rate Limiting**: Be aware of API rate limits for Yahoo Finance, OpenAI, and SerpAPI
- **Data Privacy**: Financial data should be treated as sensitive information

## 📈 Performance Considerations

- Initial data fetch: 2-5 seconds
- ML forecasting: 3-10 seconds
- LLM analysis generation: 5-15 seconds
- Total pipeline: 10-30 seconds

Cache results for frequently analyzed stocks to improve performance.

## 🐛 Troubleshooting

### Issue: "No data available for metric"
**Solution**: Ensure the company has sufficient historical data. Try fetching with a longer period.

### Issue: "API rate limit exceeded"
**Solution**: Implement rate limiting and retry logic. Check your API quota.

### Issue: "Invalid forecast result"
**Solution**: Verify that the metric series has at least 2 data points. Some companies may not have complete financial history.

## 🔄 Dependencies

- `openai` - GPT API integration
- `yfinance` - Yahoo Finance data
- `pandas` - Data manipulation
- `prophet` - Time series forecasting
- `numpy` - Numerical computing
- `scikit-learn` - Machine learning (Isolation Forest)
- `matplotlib` - Visualization
- `requests` - HTTP client

## 📝 License

[Add your license here]

## 🤝 Support

For issues, questions, or feature requests, please contact the development team or open an issue in the repository.

## 🚀 Future Enhancements

- Real-time market streaming integration
- Portfolio-level analysis across multiple stocks
- Options pricing and greeks calculation
- ESG score integration
- Sector comparison and benchmarking
- Automated alerts for risk threshold breaches
- Interactive web dashboard
- Export to PDF and Excel formats