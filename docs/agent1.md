# Financial News Analysis Agent

A Python-based financial news analyzer that leverages AI to automatically analyze and classify financial news articles. This tool uses structured prompting with OpenAI's GPT-4 to provide sentiment analysis, market impact assessment, and event detection for stock tickers.

## Features

- **Automated News Retrieval**: Fetches the latest financial news for specified stock tickers using the Polygon.io API
- **Intelligent Analysis**: Uses GPT-4 to analyze articles across multiple dimensions
- **Structured Scoring**: Provides three numerical scores:
  - **Sentiment**: -1 (very negative) to 1 (very positive)
  - **Impact**: 0 (no impact) to 1 (high impact)
  - **Relevance**: 0 (not relevant) to 1 (highly relevant)
- **Categorization**: Automatically tags articles with 15 different categories (Technology, Finance, Healthcare, etc.)
- **Event Detection**: Identifies specific financial events (Earnings Reports, M&A, Product Launches, etc.)
- **Batch Processing**: Analyzes multiple articles simultaneously with a single API call

## Installation

### Prerequisites
- Python 3.8+
- OpenAI API key
- Polygon.io API key

### Setup

1. Clone or download this repository

2. Install required dependencies:
```bash
pip install openai pydantic requests
```

3. Set environment variables:
```bash
export OPENAI_API="your_openai_api_key"
export POLYGON_API_KEY="your_polygon_io_api_key"
```

Alternatively, you can add your API keys directly in the code (not recommended for production):
```python
client = OpenAI(api_key="your_key_here")
```

## Usage

### Basic Usage

```python
from fin_news import FinNews

# Initialize the agent
agent = FinNews()

# Analyze news for a ticker
query = "What's the latest news about Apple?"
results = agent.fin_news_agent(query)
```

### Query Examples

The agent accepts natural language queries and automatically extracts:
- Stock tickers (up to 3)
- Keywords (up to 5)
- Analysis type (comprehensive, technical, fundamental)
- Forecast horizon (short_term, medium_term, long_term)

Example queries:
- "Show me recent AAPL and MSFT news with impact analysis"
- "What regulatory changes affect Tesla?"
- "Analyze semiconductor sector news for the next month"

### Output Format

The analysis returns a structured JSON response for each article:

```json
{
  "analyses": [
    {
      "article_id": "article_1",
      "article_title": "Apple Reports Record Quarterly Earnings",
      "analysis": {
        "sentiment": 0.85,
        "impact": 0.92,
        "relevance": 0.98,
        "tags": ["Technology", "Finance", "Economics"],
        "event_detection": ["Earnings Report"],
        "reasoning": "Apple's record earnings significantly exceed analyst expectations, signaling strong market demand and pricing power. This represents a major positive catalyst with potential for 5%+ stock price appreciation. The news is directly focused on Apple's financial performance."
      }
    }
  ]
}
```

## API Reference

### Main Classes

#### `FinNews`
Main agent class that orchestrates the news analysis workflow.

**Methods:**
- `fin_news_agent(query: str) -> List[BatchNewsAnalysisResponse]`: Analyzes news based on a natural language query

#### `ArticleAnalysis`
Pydantic model containing analysis scores and classifications for a single article.

**Fields:**
- `sentiment`: float (-1 to 1)
- `impact`: float (0 to 1)
- `relevance`: float (0 to 1)
- `tags`: List[TagCategory]
- `event_detection`: List[EventType]
- `reasoning`: str

#### `TagCategory` (Enum)
Available article categories: Technology, Finance, Healthcare, Energy, Consumer, Industrial, Real Estate, Materials, Telecommunications, Utilities, Politics, Economics, Regulatory, ESG, Cryptocurrency

#### `EventType` (Enum)
Detectable financial events: Earnings Report, Merger & Acquisition, Product Launch, Partnership, Regulatory Change, Leadership Change, Market Movement, Legal Issue, Financial Guidance, None

### Key Functions

#### `agent_understand(query: str) -> dict`
Parses natural language queries and extracts structured parameters using GPT.

**Returns:**
```json
{
  "ticker": ["AAPL", "MSFT"],
  "keywords": ["earnings", "growth"],
  "analysis_type": "comprehensive",
  "forecast_horizon": "medium_term",
  "currency": "USD"
}
```

#### `get_data(limit: int, keyword: str) -> List[dict]`
Fetches news articles from Polygon.io API.

**Parameters:**
- `limit`: Maximum number of articles to retrieve
- `keyword`: Stock ticker symbol

**Returns:** List of article objects with metadata

#### `get_resp(articles: List[dict]) -> BatchNewsAnalysisResponse`
Sends articles to GPT-4 for structured analysis and classification.

## Scoring Guide

### Sentiment Score Interpretation
- **-1 to -0.3**: Bearish (negative for markets) - e.g., rate hikes, poor earnings, regulatory crackdowns
- **-0.3 to 0.3**: Neutral (mixed signals or uncertain impact)
- **0.3 to 1**: Bullish (positive for markets) - e.g., rate cuts, strong earnings, favorable policy

### Impact Score Interpretation
- **0 to 0.3**: Low impact (< 1-2% price movement expected)
- **0.3 to 0.7**: Medium impact (2-5% price movement expected)
- **0.7 to 1**: High impact (> 5% price movement expected)

### Relevance Score Interpretation
- **0 to 0.3**: Low relevance (ticker mentioned in passing)
- **0.3 to 0.7**: Medium relevance (ticker affected indirectly)
- **0.7 to 1**: High relevance (news directly about the ticker)

## Configuration

### Batch Size
Currently configured to fetch 2 articles per ticker. Modify the `get_data()` call in `fin_news_agent()`:
```python
all_data = get_data(10, ticker)  # Fetch up to 10 articles
```

### Models
- **News Analysis**: GPT-4o-mini (can be changed to gpt-4, gpt-4-turbo)
- **Query Understanding**: GPT-5-mini (note: verify model availability)

## Error Handling

The code uses Pydantic for validation. Common errors include:

- **Invalid API Keys**: Verify keys are set correctly
- **Rate Limiting**: Polygon.io and OpenAI have rate limits; implement retry logic if needed
- **Empty Results**: If no articles are found for a ticker, the API returns empty results
- **Validation Errors**: Ensure analysis scores fall within expected ranges (-1 to 1, 0 to 1)

## Limitations

- Batch processing limited to multiple articles per API call (adjust based on token limits)
- Ticker extraction limited to 3 symbols per query
- Keyword extraction limited to 5 terms
- Dependent on external APIs (Polygon.io, OpenAI) for functionality

## Security Notes

⚠️ **API Keys**: Never hardcode API keys in production. Use environment variables or secure key management systems.

## Future Enhancements

- Add caching for frequently analyzed articles
- Implement retry logic with exponential backoff
- Add support for historical analysis
- Enhanced error handling and logging
- Support for additional data sources
- Real-time streaming analysis

## Dependencies

- `openai` - OpenAI API client
- `pydantic` - Data validation and serialization
- `requests` - HTTP library for API calls
- `json` - JSON parsing
- `enum` - Enumeration support
- `os` - Environment variables

## License

[Add your license here]

## Support

For issues or questions, please contact the development team or open an issue in the repository.