# Polymarket Reddit Agent

An AI-powered prediction market analysis tool that combines Polymarket data with Reddit sentiment analysis to generate actionable trade recommendations. Uses GPT to extract keywords, search markets and discussions, and synthesize insights into structured trade calls.

## Features

- **Natural Language Queries**: Convert user questions into actionable market searches
- **Dual Data Source Integration**: Combines Polymarket API data with Reddit sentiment analysis
- **AI-Powered Sentiment Analysis**: Uses GPT to detect market inefficiencies between odds and social sentiment
- **Structured Trade Calls**: Generates comprehensive trade recommendations with confidence scores and risk assessment
- **Keyword Extraction**: Intelligently extracts primary keywords, market search terms, and Reddit queries from user input
- **Multi-Subreddit Search**: Searches across politics, news, worldnews, cryptocurrency, and technology communities

## Requirements

- Python 3.9+
- OpenAI API key
- Reddit API credentials (client ID, client secret, user agent)
- praw (Python Reddit API Wrapper)
- pydantic
- requests

## Installation

1. Clone the repository or download the code
2. Install dependencies:
   ```bash
   pip install praw pydantic requests openai
   ```

3. Set up environment variables:
   ```bash
   export OPENAI_API_KEY="your-openai-api-key"
   export REDDIT_CLIENT_ID="your-reddit-client-id"
   export REDDIT_CLIENT_SECRET="your-reddit-client-secret"
   export REDDIT_USER_AGENT="YourApp/1.0 by YourUsername"
   ```

## Reddit API Setup

To use the Reddit integration, you need to create a Reddit app:

1. Go to https://www.reddit.com/prefs/apps
2. Click "Create an app" or "Create another app"
3. Fill in the details:
   - **Name**: Your app name
   - **App type**: Select "script"
   - **Redirect URI**: http://localhost:8080
4. Copy your **Client ID**, **Client Secret**, and create a **User Agent** string

## Enums & Configuration

### Call Types
- `BUY` - Strong bullish signal
- `SELL` - Strong bearish signal
- `HOLD` - Neutral, wait for more signals
- `ARBITRAGE` - Market inefficiency detected

### Confidence Levels
- `HIGH` - Strong signal with high conviction
- `MEDIUM` - Moderate confidence
- `LOW` - Weak signal, needs monitoring

### Positions
- `YES` - Bet on positive outcome
- `NO` - Bet on negative outcome

### Position Sizes
- `SMALL` - Conservative allocation
- `MEDIUM` - Standard allocation
- `LARGE` - Aggressive allocation

### Sentiment Signals
- `BULLISH` - Strong positive Reddit sentiment
- `BEARISH` - Strong negative Reddit sentiment
- `NEUTRAL` - Balanced sentiment
- `MIXED` - Conflicting signals

### Catalyst Types
- `NEWS` - News-driven price movement
- `REDDIT_TREND` - Social media trending
- `MISPRICING` - Market inefficiency
- `ARBITRAGE` - Cross-platform opportunity
- `MOMENTUM` - Technical momentum signal

### Urgency Levels
- `IMMEDIATE` - Act now, time-sensitive
- `NEAR_TERM` - Within days/week
- `MONITOR` - Watch for developments

## Usage

### Basic Example

```python
from polymarket_reddit_agent import PolymarketRedditAgent
import os

# Initialize the agent
agent = PolymarketRedditAgent(
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    reddit_client_id=os.getenv("REDDIT_CLIENT_ID"),
    reddit_client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    reddit_user_agent=os.getenv("REDDIT_USER_AGENT")
)

# Analyze a prediction market query
user_query = "Will Bitcoin reach $100k by end of year?"
trade_calls = agent.analyze_from_query(user_query)

# Access trade call details
for call in trade_calls:
    print(f"Market: {call.market_question}")
    print(f"Recommendation: {call.call_type.value}")
    print(f"Position: {call.recommended_position.value}")
    print(f"Confidence: {call.confidence.value}")
    print(f"Reasoning: {call.reasoning}")
    print(f"Urgency: {call.urgency.value}")
    print(f"Risk Factors: {', '.join(call.risk_factors)}")
    print("---")

# Save to JSON
agent.save_calls_to_json(trade_calls, 'my_analysis.json')
```

## Output Structure

The `analyze_from_query()` method returns a list of `TradeCall` objects with:

- `call_type` - Trade recommendation (BUY, SELL, HOLD, ARBITRAGE)
- `confidence` - Confidence level of the recommendation
- `market_id` - Unique identifier of the Polymarket market
- `market_question` - The prediction market question
- `current_odds` - YES and NO probabilities
- `recommended_position` - Which side to take (YES or NO)
- `suggested_size` - Position size recommendation
- `reasoning` - Detailed explanation of the recommendation
- `sentiment_score` - Aggregate sentiment (-1 to +1)
- `reddit_signal` - Overall Reddit sentiment
- `catalyst_type` - Primary driver of the recommendation
- `urgency` - Time sensitivity of the trade
- `risk_factors` - Key risks to consider
- `key_reddit_threads` - Top 3 relevant Reddit discussions
- `timestamp` - Analysis timestamp

## API Reference

### PolymarketRedditAgent

#### `__init__(openai_api_key, reddit_client_id, reddit_client_secret, reddit_user_agent)`
Initialize the agent with API credentials.

#### `analyze_from_query(user_query: str) -> List[TradeCall]`
Main entry point. Processes a user query through the full analysis pipeline and returns trade recommendations.

#### `save_calls_to_json(trade_calls: List[TradeCall], filename: str) -> str`
Export trade calls to JSON format.

### PolymarketClient

#### `search_markets_by_keywords(keywords: List[str], limit: int) -> List[dict]`
Search Polymarket for markets matching keywords. Returns unique markets sorted by relevance.

#### `get_market_details(market_id: str) -> dict`
Fetch detailed information for a specific market.

### RedditClient

#### `search_with_keywords(keywords: List[str], subreddits: List[str], limit: int) -> List[dict]`
Search Reddit across multiple subreddits for relevant discussions. Returns sorted by upvote score.

### AIAnalyzer

#### `extract_keywords_from_query(user_query: str) -> SearchKeywords`
Uses GPT to extract primary keywords, market search terms, and Reddit queries from natural language input.

#### `analyze_market_sentiment(market_data: dict, reddit_threads: List[dict], user_query: str) -> TradeCall`
Synthesizes market data and Reddit sentiment into a structured trade recommendation.

## Analysis Pipeline

The agent processes queries through four main steps:

1. **Keyword Extraction**: AI converts natural language into structured search terms
2. **Market Search**: Finds relevant prediction markets on Polymarket
3. **Reddit Analysis**: Searches Reddit for related discussions and sentiment
4. **Trade Generation**: Combines all signals into actionable trade recommendations

## Error Handling

- Market search errors are logged but don't halt the pipeline
- Reddit API errors (rate limiting, search failures) are caught and reported
- Invalid market data gracefully defaults to neutral odds (0.5)
- Missing Reddit discussions don't prevent analysis

## Rate Limiting & Best Practices

- Reddit API has rate limits (~60 requests/minute)
- Polymarket API may throttle frequent requests
- Consider spacing out multiple queries
- Cache results when possible to avoid redundant searches

## Limitations

- Reddit sentiment may not reflect all market participants
- Polymarket search may not find all relevant markets
- AI analysis is probabilistic and may miss important factors
- Past sentiment/predictions do not guarantee future outcomes
- Requires valid Reddit app credentials with proper redirect URI

## Important Disclaimer

This tool is for informational and analytical purposes only. Prediction market trading involves significant financial risk. Always conduct your own research, manage position sizes appropriately, and only risk capital you can afford to lose. This is not financial advice, and trading decisions should be made carefully and with full understanding of the risks involved.

## Support

For issues, questions, or feature requests, please refer to the documentation or contact the development team.