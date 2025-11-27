# Fashion Shopping Agent

An AI-powered shopping assistant that generates personalized fashion recommendations based on user preferences, style, and lifestyle. Combines GPT language models with real-time product search to deliver curated shopping suggestions across multiple categories.

## Features

- **AI-Powered Style Analysis**: Uses GPT to understand user preferences and generate personalized fashion recommendations
- **Multi-Category Search**: Searches across tops, bottoms, footwear, and accessories
- **Real-Time Product Discovery**: Integrates with Google Shopping API via SerpAPI for live product availability and pricing
- **Structured Recommendations**: Returns organized JSON with curated products, prices, ratings, and links
- **Location-Aware Pricing**: Generates price recommendations in local currency based on user location
- **Gender-Specific Results**: Tailors recommendations based on user gender preference
- **Smart Filtering**: Limits results to top 3 items per keyword for focused recommendations
- **Price Range Support**: Includes min/max price recommendations based on budget

## Requirements

- Python 3.9+
- OpenAI API key
- SerpAPI key (for Google Shopping integration)
- FastAPI (optional, for API deployment)
- Pydantic
- Requests
- LanceDB (vector database support)

## Installation

1. Install dependencies:
   ```bash
   pip install requests openai pydantic fastapi lancedb python-dotenv
   ```

2. Set up environment variables:
   ```bash
   export OPENAI_API_KEY="your-openai-api-key"
   export SERPAPI_KEY="your-serpapi-key"
   ```

3. Store your API keys securely (do not commit to version control):
   ```bash
   # Create a .env file
   OPENAI_API_KEY=your-key-here
   SERPAPI_KEY=your-key-here
   ```

## API Keys

### OpenAI API
- Get key from: https://platform.openai.com/api-keys
- Used for: Natural language processing and style recommendations
- Scope: Create chat completions with GPT models

### SerpAPI Key
- Get key from: https://serpapi.com
- Used for: Real-time Google Shopping searches
- Scope: Query shopping results, product information, pricing

## Usage

### Basic Example

```python
from shopping_agent import ShoppingAgent
import os

# Initialize the agent
api_key = os.getenv("SERPAPI_KEY")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

user_prompt = """
I'm a 28-year-old professional who works in tech. 
I prefer minimalist, modern clothing in neutral colors. 
I need versatile pieces for both office and casual wear. 
Budget: $500-$2000. I'm based in the US.
"""

agent = ShoppingAgent(
    api_key=api_key,
    client=client,
    vectors=None,  # For future vector DB integration
    user_prompt=user_prompt
)

# Get personalized recommendations
products = agent.get_products()
print(products)
```

### Getting Style Keywords

```python
# Get AI-generated shopping keywords
keywords = agent.get_shop()
print(keywords)
# Output: JSON with categorized fashion items and price ranges
```

### Output Structure

```python
{
    "top": [
        "casual t-shirt",
        "oxford button-down",
        "minimalist sweater"
    ],
    "bottom": [
        "slim-fit chinos",
        "dark jeans",
        "neutral trousers"
    ],
    "footwear": [
        "white minimalist sneaker",
        "brown leather loafer",
        "neutral canvas shoe"
    ],
    "accessories": [
        "leather watch",
        "minimalist bag",
        "leather belt"
    ],
    "gender": "male",
    "min_price": 500,
    "max_price": 2000,
    "location": "United States"
}
```

### Product Results Format

```python
{
    "top": {
        "casual t-shirt": {
            "items": [
                {
                    "title": "Premium Cotton T-Shirt",
                    "source": "example.com",
                    "price": "$29.99",
                    "rating": 4.5,
                    "image_url": "https://..."
                },
                # ... more items
            ]
        },
        # ... more keywords
    },
    # ... other categories
}
```

## API Reference

### ShoppingAgent

#### `__init__(api_key: str, client: OpenAI, vectors: Optional[Any], user_prompt: str)`
Initialize the shopping agent with API credentials and user preferences.

**Parameters:**
- `api_key` - SerpAPI key for Google Shopping searches
- `client` - OpenAI client instance
- `vectors` - Vector database instance (for future enhancements)
- `user_prompt` - User's style preferences and requirements

#### `llm_chat(model: str = "gpt-5-mini") -> str`
Generate shopping keywords using GPT based on user prompt.

**Returns:** JSON string with categorized fashion keywords and pricing

#### `get_shop() -> str`
Wrapper method to retrieve AI-generated shopping keywords.

**Returns:** JSON string with style recommendations

#### `get_products() -> Dict`
Fetch real products from Google Shopping for all recommended keywords.

**Returns:** Nested dictionary with products organized by category and keyword

**Fetches:**
- Product title
- Source/retailer
- Price
- Rating
- Product image URL

#### `get_product_link() -> List`
Retrieve immersive product results from Google Shopping (experimental).

**Returns:** List of detailed product results

### Utility Functions

#### `sync_fashion() -> Dict`
Convenience function to initialize agent and fetch all products in one call.

**Returns:** Complete product recommendations dictionary

## Configuration

### Prompt Customization

The agent uses a sophisticated prompt template that:
- Emphasizes user input as primary source
- Falls back to context and order history if info is missing
- Generates 3 items per category maximum
- Includes practical, minimalist, and modern items
- Focuses on neutral colors and versatile styles
- Targets casual, professional, and leisure settings

### Category Limits

Each category is limited to 3 items per keyword:
- `top`: max 3 items
- `bottom`: max 3 items
- `footwear`: max 3 items
- `accessories`: max 3 items

### Price Recommendations

- System generates local currency prices based on location
- Includes both minimum and maximum budget
- Helps users find products within their price range

## Error Handling

The system includes robust error handling:

```python
# API request failures are caught and logged
try:
    response = requests.get(url, params=params)
    response.raise_for_status()
except Exception as e:
    print(f"Error fetching products: {e}")

# JSON parsing errors are handled gracefully
try:
    shop = json.loads(response_text)
except Exception as e:
    print(f"Error parsing recommendations: {e}")
```

## Rate Limiting

The system includes built-in rate limiting:

```python
time.sleep(1)  # 1 second delay between API requests
```

This prevents hitting SerpAPI rate limits when searching multiple keywords.

## Best Practices

1. **Detailed User Prompts**: Provide comprehensive style information for better recommendations
   ```
   ✓ "28-year-old professional, minimalist style, tech industry, budget $1000"
   ✗ "I need clothes"
   ```

2. **Budget Clarity**: Always specify min/max price in your prompt
   - Helps filter results appropriately
   - Ensures recommendations match financial constraints

3. **Location Specification**: Include your location for:
   - Local currency pricing
   - Regional product availability
   - Relevant shipping information

4. **API Key Security**:
   - Never hardcode API keys in source files
   - Use environment variables
   - Rotate keys periodically
   - Keep keys out of version control

5. **Batch Processing**: When processing multiple user requests:
   ```python
   for user_prompt in user_prompts:
       agent = ShoppingAgent(api_key, client, None, user_prompt)
       products = agent.get_products()
       # Process results
       time.sleep(2)  # Respect rate limits
   ```

## Limitations

- Google Shopping API availability varies by region
- Product availability and pricing change frequently
- Some keywords may return limited or no results
- Image URLs may become invalid over time
- Ratings may not always be present for all products
- Shopping results depend on SerpAPI coverage

## Future Enhancements

- Vector database integration for better product matching
- Order history integration for learning user preferences
- Multi-language support
- Color preference detection and filtering
- Size recommendation based on past purchases
- Social media style integration
- Virtual try-on capabilities
- Price tracking and deal notifications
- Sustainability/ethical brand filtering

## Troubleshooting

### "Error: API key not found"
- Ensure environment variables are set correctly
- Verify keys in your .env file
- Restart your terminal or IDE

### "No shopping results found"
- Try more specific keyword combinations
- Check location setting is correct
- Verify SerpAPI subscription is active

### "Rate limit exceeded"
- Increase sleep duration between requests
- Check your SerpAPI usage quota
- Consider upgrading your plan

### "Invalid JSON from LLM"
- The system will retry automatically
- Check your OpenAI API quota
- Verify model name is available

## Integration with FastAPI

```python
from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse

router = APIRouter()

@router.post("/shopping/recommendations")
async def get_recommendations(
    user_prompt: str = Body(..., embed=True)
):
    agent = ShoppingAgent(
        api_key=os.getenv("SERPAPI_KEY"),
        client=OpenAI(api_key=os.getenv("OPENAI_API_KEY")),
        vectors=None,
        user_prompt=user_prompt
    )
    products = agent.get_products()
    return JSONResponse(content=products)
```

## Important Disclaimer

This tool is designed for shopping assistance purposes only. Always verify product details, pricing, and authenticity directly on retailer websites before making purchases. The agent does not guarantee product availability, accuracy of pricing, or retailer credibility. Shopping decisions should be made independently with thorough research.

## Support

For issues or questions:
- Check API documentation: OpenAI (https://platform.openai.com/docs) and SerpAPI (https://serpapi.com/docs)
- Review error messages and logs
- Verify API keys and permissions
- Check rate limit usage in API dashboards