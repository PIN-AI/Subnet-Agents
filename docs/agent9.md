# AI Travel Planner

An intelligent travel planning assistant that leverages AI and real-time data to create personalized travel itineraries. Combines GPT recommendations with live flight searches, hotel booking options, weather forecasts, and curated attractions to deliver comprehensive travel plans.

## Features

- **AI-Powered Destination Selection**: GPT analyzes user preferences to recommend ideal cities
- **Real-Time Flight Search**: Integrates Google Flights API via SerpAPI for current prices and schedules
- **Hotel Booking Integration**: Searches available accommodations with ratings and amenities
- **Weather-Aware Planning**: Fetches forecasts to optimize travel dates
- **Dynamic Itinerary Generation**: Creates multi-day themed itineraries with morning/afternoon/evening activities
- **Transit Information**: Google Maps directions for getting around destinations
- **Local Attractions**: Discovers top tourist attractions and local places of interest
- **Multi-City Support**: Plans trips across multiple cities in the same country
- **Currency Localization**: Displays prices in user's local currency

## Requirements

- Python 3.9+
- OpenAI API key
- SerpAPI key (for Google Flights, Hotels, Maps, and Search)
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
- Used for: Destination recommendations and itinerary generation
- Scope: Create chat completions with GPT models

### SerpAPI Key
- Get key from: https://serpapi.com
- Used for: Flights, hotels, weather, directions, and local attractions
- Scope: Query multiple search engines (Google Flights, Hotels, Maps, Local)

## Usage

### Basic Example

```python
from travel_planner import TravelPlanner
import os

user_prompt = """
I'm planning a 10-day trip to India in October 2025.
I love cultural sites, historical monuments, and spiritual experiences.
I prefer a mix of popular and off-the-beaten-path destinations.
Budget: $2000-5000 USD.
I'm based in the US and my origin airport is JFK.
I travel with my spouse, so I need double occupancy.
"""

planner = TravelPlanner(
    api_key=os.getenv("SERPAPI_KEY"),
    client=OpenAI(api_key=os.getenv("OPENAI_API_KEY")),
    user_prompt=user_prompt
)

# Generate complete travel plan
travel_plan = planner.make_plan()
print(travel_plan)
```

### Step-by-Step Usage

```python
# Step 1: Get destination recommendations
destinations = json.loads(planner.fetch_dest())
print(destinations)
# Output: Recommended cities, currency, origin airport

# Step 2: Fetch weather and optimize dates
dates = json.loads(planner.fetch_dates())
print(dates)
# Output: Recommended travel date ranges per city

# Step 3: Search flights
flights = planner.fetch_flights(
    origin="JFK",
    destination="DEL",
    currency="USD",
    departure_date="2025-10-15"
)
print(flights)

# Step 4: Find hotels
hotels = planner.fetch_hotels(
    location="New Delhi",
    check_in_date="2025-10-15",
    check_out_date="2025-10-18",
    currency="USD",
    adults=2
)
print(hotels)

# Step 5: Generate itinerary
itinerary = planner.make_itenary(city="New Delhi", days=3)
print(itinerary)
```

### Convenience Function

```python
from travel_planner import sync_travel

user_prompt = "I want a relaxing beach vacation in Bali for 5 days next month"
complete_plan = sync_travel(user_prompt)
print(complete_plan)
```

## Output Structure

### Complete Travel Plan

```python
{
    "city": "New Delhi",
    "days": 3,
    "description": "Capital city known for historical monuments and cultural heritage",
    "flights": [
        [
            {
                "airline": "IndiGo",
                "price": "$450",
                "route": [
                    {
                        "from": "New York (JFK)",
                        "departure_time": "10:00 PM",
                        "to": "New Delhi (DEL)",
                        "arrival_time": "12:30 AM+1"
                    }
                ]
            }
        ]
    ],
    "hotels": [
        {
            "name": "Hotel Taj Palace",
            "type": "Hotel",
            "description": "Luxury hotel in central New Delhi",
            "rate_per_night": "$120",
            "total_rate": "$360",
            "overall_rating": 4.5,
            "location_rating": 4.8,
            "amenities": ["WiFi", "Pool", "Gym", "Restaurant"],
            "images": ["url1", "url2", "url3"],
            "link": "https://...",
            "nearby_places": [
                {"name": "India Gate"},
                {"name": "Rashtrapati Bhawan"}
            ]
        }
    ],
    "itinerary": {
        "days": [
            {
                "day": 1,
                "theme": "Heritage & Culture",
                "activities": [
                    {
                        "time": "Morning",
                        "title": "Red Fort",
                        "description": "Historic fort complex built by Mughal emperor Shah Jahan",
                        "image": "https://..."
                    },
                    {
                        "time": "Afternoon",
                        "title": "Jama Masjid",
                        "description": "One of India's largest mosques with stunning architecture",
                        "image": "https://..."
                    },
                    {
                        "time": "Evening",
                        "title": "Chandni Chowk Market",
                        "description": "Historic street market with street food and shopping",
                        "image": "https://..."
                    }
                ]
            }
        ]
    }
}
```

## API Reference

### TravelPlanner

#### `__init__(api_key: str, client: OpenAI, user_prompt: str)`
Initialize the travel planner with API credentials and user preferences.

**Parameters:**
- `api_key` - SerpAPI key for travel searches
- `client` - OpenAI client instance
- `user_prompt` - User's travel preferences and requirements

#### `fetch_dest() -> str`
Get AI-recommended destinations based on user preferences.

**Returns:** JSON string with recommended cities, origin, currency, and descriptions

#### `fetch_weather(city: str) -> List[Dict]`
Get weather forecast for a city.

**Returns:** List of date-weather mappings for the next 10 days

#### `fetch_dates() -> str`
Generate optimal travel dates based on calendar availability and weather.

**Returns:** JSON with city codes mapped to recommended date ranges

#### `fetch_flights(origin: str, destination: str, currency: str, departure_date: str) -> List[Dict]`
Search for flights between two airports.

**Parameters:**
- `origin` - IATA code of departure airport
- `destination` - IATA code of arrival airport
- `currency` - Currency for pricing
- `departure_date` - Date in YYYY-MM-DD format

**Returns:** List of flight options with airlines, prices, and routes

#### `fetch_hotels(location: str, check_in_date: str, check_out_date: str, currency: str, adults: int = 2) -> List[Dict]`
Search for hotels in a destination.

**Parameters:**
- `location` - City or hotel location name
- `check_in_date` - Date in YYYY-MM-DD format
- `check_out_date` - Date in YYYY-MM-DD format
- `currency` - Currency for pricing
- `adults` - Number of adult guests

**Returns:** List of hotels with rates, amenities, ratings, and images

#### `fetch_transit(start_addr: str, end_addr: str) -> Dict`
Get transit directions between two locations.

**Returns:** Google Maps directions data with routes and travel times

#### `fetch_popular(location: str, days: int) -> List[Dict]`
Get popular tourist attractions for a city.

**Parameters:**
- `location` - City name
- `days` - Number of days (used to limit results)

**Returns:** List of top attractions

#### `fetch_localplaces(q: str, location: str) -> List[Dict]`
Search for local places by category and location.

**Parameters:**
- `q` - Query term (e.g., "restaurants", "museums")
- `location` - Location coordinates or name

**Returns:** List of local businesses/places

#### `make_itenary(city: str, days: int) -> Dict`
Generate a multi-day themed itinerary for a city.

**Returns:** JSON with daily themes and morning/afternoon/evening activities

#### `travel() -> None`
Fetch all travel data (flights, hotels, itineraries). Populates internal attributes.

#### `make_plan() -> Dict`
Generate complete travel plan combining all data.

**Returns:** Comprehensive travel plan with flights, hotels, and itineraries

### Utility Functions

#### `sync_travel(user_prompt: str) -> Dict`
Convenience function to generate complete travel plan in one call.

**Parameters:**
- `user_prompt` - User's travel preferences

**Returns:** Complete travel plan

## Best Practices

### User Prompt Guidelines

Provide comprehensive travel information for better recommendations:

```python
✓ Good prompt:
"I want a 7-day cultural tour of Japan in spring (March-April). 
I love temples, gardens, and local cuisine. 
Budget: $3000-5000 USD.
I prefer moderate pace with mix of guided tours and free exploration.
Origin: San Francisco (SFO).
I travel with my family (2 adults, 1 child)."

✗ Poor prompt:
"I want to go to Japan"
```

### Key Information to Include

1. **Duration**: How many days/weeks
2. **Timeframe**: Specific dates or season
3. **Travel Style**: Adventure, relaxation, culture, food, etc.
4. **Activities**: What you want to do
5. **Budget**: Min-max price range
6. **Origin**: Your home airport or city
7. **Group Size**: Solo, couple, family, etc.
8. **Climate Preference**: Hot, cold, mild, etc.

### API Rate Limiting

```python
# The system includes rate limiting, but for batch processing:
import time

for user in users:
    plan = sync_travel(user['prompt'])
    time.sleep(2)  # Respect rate limits
```

### Currency Handling

- Always specify your home currency in the prompt
- Flight and hotel prices will be shown in local currency
- Exchange rates are current at time of API call

## Output Formats

### IATA Airport Codes
All destinations and origins use IATA codes:
- JFK: New York
- LHR: London
- NRT: Tokyo
- DEL: New Delhi
- BLR: Bangalore

### Date Format
All dates use YYYY-MM-DD format:
- "2025-10-15" (October 15, 2025)
- Date ranges: "2025-10-15 to 2025-10-18"

## Error Handling

The system handles common errors gracefully:

```python
# Missing hotel availability
if hotels is None:
    print("No hotels found for the selected dates")

# Flight search failure
if flights is None:
    print("No flights available for this route")

# Weather data unavailable
try:
    weather = planner.fetch_weather(city)
except Exception as e:
    print(f"Weather unavailable: {e}")
```

## Limitations

- Limited to planning trips within a single country
- Maximum of 4 cities per trip recommendation
- Weather data available for next 10 days only
- Flight search limited to future dates
- Hotel availability depends on SerpAPI coverage
- Image URLs may become outdated
- Some destinations may have limited data availability
- Itinerary themes are AI-generated and may vary

## Future Enhancements

- Multi-country trip planning
- Budget breakdown and tracking
- Real-time booking integration
- Travel insurance recommendations
- Visa requirement checker
- Currency exchange rate updates
- Social media travel companion finder
- Real-time flight price alerts
- Restaurant reservation integration
- Activity booking integration
- Travel document checklist
- Transportation pass recommendations
- Local event discovery
- Carbon footprint calculator
- Travel insurance comparison

## Troubleshooting

### "No flights found"
- Verify origin and destination IATA codes
- Check if date is in the future
- Try a different departure date
- Ensure currency code is correct

### "No hotels available"
- Try extending the date range
- Search in nearby cities
- Verify location name spelling
- Check if property type matches needs

### "Weather data unavailable"
- City name may be misspelled
- Try with country name included
- Some locations have limited coverage

### "Invalid JSON response"
- Check OpenAI API quota
- Verify model name is available
- Try again in a few moments

## Integration with FastAPI

```python
from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse

router = APIRouter()

@router.post("/travel/plan")
async def create_travel_plan(
    user_prompt: str = Body(..., embed=True)
):
    plan = sync_travel(user_prompt)
    return JSONResponse(content=plan)

@router.get("/travel/weather/{city}")
async def get_city_weather(city: str):
    planner = TravelPlanner(
        api_key=os.getenv("SERPAPI_KEY"),
        client=OpenAI(api_key=os.getenv("OPENAI_API_KEY")),
        user_prompt=""
    )
    weather = planner.fetch_weather(city)
    return JSONResponse(content=weather)
```

## Security Considerations

1. **Never hardcode API keys** - Use environment variables
2. **Protect user data** - Don't store personal travel information in logs
3. **Validate inputs** - Sanitize user prompts before processing
4. **Rate limiting** - Implement rate limiting on API endpoints
5. **HTTPS only** - Always use HTTPS for API communications

## Important Disclaimer

This tool provides travel planning assistance for informational purposes. Always verify:
- Flight times and prices directly with airlines
- Hotel availability and rates on booking platforms
- Visa requirements with official government sources
- Travel advisories with your government
- Insurance coverage for your destination
- Current health and safety guidelines

The planner should be used as a starting point for research, not as a definitive booking source. Always double-check all information before making travel bookings or commitments.

## Support

For issues or questions:
- Check OpenAI API documentation: https://platform.openai.com/docs
- Review SerpAPI documentation: https://serpapi.com/docs
- Verify API keys and permissions
- Check rate limit usage in API dashboards
- Review error messages and logs for debugging