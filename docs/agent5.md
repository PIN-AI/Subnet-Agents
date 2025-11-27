# Stock Analysis Agent

An AI-powered stock analysis and prediction tool that leverages natural language processing to extract stock information, fetch historical data, predict future prices, and generate investment recommendations.

## Features

- **Natural Language Processing**: Extract structured stock information from plain English queries
- **Historical Data Retrieval**: Fetch real-time and historical stock data from Yahoo Finance
- **Price Prediction**: LagLlama-style time series predictions with confidence scoring
- **AI Recommendations**: Generate buy/sell recommendations with reasoning using OpenAI's GPT models
- **Structured Output**: Uses Pydantic models for reliable data validation and type safety

## Requirements

- Python 3.9+
- OpenAI API key
- yfinance
- pandas
- numpy
- pydantic

## Installation

1. Clone the repository or download the code
2. Install dependencies:
   ```bash
   pip install openai yfinance pandas numpy pydantic
   ```

3. Set up your environment variables:
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```

## Configuration

### Supported Currencies

- USD (US Dollar)
- EUR (Euro)
- GBP (British Pound)
- JPY (Japanese Yen)
- CNY (Chinese Yuan)
- AUD (Australian Dollar)
- CAD (Canadian Dollar)
- INR (Indian Rupee)

### Supported Time Intervals

- `1h` - 1 hour
- `1d` - 1 day
- `5d` - 5 days
- `1wk` - 1 week
- `1mo` - 1 month
- `3mo` - 3 months

### Recommendation Levels

- `STRONG_BUY` - Highly recommended to buy
- `BUY` - Recommended to buy
- `HOLD` - Hold current position
- `SELL` - Recommended to sell
- `STRONG_SELL` - Strongly recommended to sell

## Usage

### Basic Example

```python
from stock_analysis_agent import StockAnalysisAgent

# Initialize the agent
agent = StockAnalysisAgent(openai_api_key="your-api-key")

# Analyze a stock with natural language query
query = "Should I buy Apple stock? I want daily data in USD"
analysis = agent.analyze(query)

# Access results
print(f"Current Price: ${analysis.prediction.current_price:.2f}")
print(f"Predicted Price: ${analysis.prediction.predicted_price:.2f}")
print(f"Recommendation: {analysis.recommendation.value}")
print(f"Reasoning: {analysis.reasoning}")
```

### Output Structure

The `analyze()` method returns a `StockAnalysis` object containing:

- `query` - Parsed stock query details
- `historical_data` - DataFrame with historical price data
- `prediction` - Price prediction with confidence score
- `recommendation` - Buy/Sell recommendation (STRONG_BUY, BUY, HOLD, SELL, STRONG_SELL)
- `score` - Confidence score (0-100)
- `reasoning` - AI-generated explanation for the recommendation
- `timestamp` - Analysis timestamp in ISO format

## How It Works

The analysis pipeline consists of four main steps:

1. **Information Extraction**: Parses natural language queries to extract company name, ticker symbol, country, currency, and time interval

2. **Data Retrieval**: Fetches 60 days of historical stock data from Yahoo Finance (configurable)

3. **Price Prediction**: Uses a simplified LagLlama-style approach analyzing short-term and long-term moving averages to predict future prices with volatility-adjusted confidence

4. **Recommendation Generation**: Leverages OpenAI's GPT model to analyze all factors and generate a structured investment recommendation

## API Reference

### StockAnalysisAgent

#### `__init__(openai_api_key: str)`
Initialize the agent with your OpenAI API key.

#### `extract_stock_info(user_query: str) -> StockQuery`
Extract structured stock information from a natural language query.

#### `fetch_historical_data(query: StockQuery, lookback_days: int = 60) -> pd.DataFrame`
Fetch historical stock data from Yahoo Finance.

#### `predict_with_lagllama(historical_data: pd.DataFrame) -> StockPrediction`
Generate price predictions based on historical data.

#### `generate_recommendation(query: StockQuery, historical_data: pd.DataFrame, prediction: StockPrediction) -> tuple[Recommendation, float, str]`
Generate buy/sell recommendation with reasoning.

#### `analyze(user_query: str) -> StockAnalysis`
Run the complete analysis pipeline on a user query.

## Error Handling

The agent validates all inputs and raises informative errors:

- `ValueError` - Raised when no historical data is found for a ticker
- `OpenAI API errors` - Handled by the OpenAI client
- Invalid ticker symbols are detected during data fetching

## Limitations

- Predictions are simplified and based on moving averages; not suitable for financial decision-making without additional analysis
- Historical data lookback is limited to 60 days by default (configurable)
- Requires valid ticker symbols as recognized by Yahoo Finance
- API rate limits apply based on your OpenAI account tier

## Important Disclaimer

This tool is for informational and educational purposes only. It should not be used as the sole basis for investment decisions. Always consult with a qualified financial advisor before making investment decisions. Past performance does not guarantee future results.

## License

[Specify your license here]

## Support

For issues or questions, please refer to the documentation or contact the development team.