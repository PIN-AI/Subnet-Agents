# AI-Powered Food Planner

An intelligent meal recommendation engine that combines real-time food trend analysis, nutritional information, restaurant discovery, and AI-driven personalization to suggest the perfect meal based on user preferences, dietary requirements, time of day, and location.

## 🍽️ Features

- **Smart Meal Recommendations**: AI-powered suggestions based on time of day, location, and preferences
- **Real-Time Food Trends**: Search trending dishes and cuisines via SerpAPI
- **Nutritional Information**: Automatic fetching of comprehensive nutrition facts
- **Restaurant Discovery**: Find nearby restaurants serving your recommended dish
- **Dietary Preferences**: Support for vegetarian, non-vegetarian, vegan, and custom dietary needs
- **Location-Based Search**: Tailored recommendations based on geographic location
- **Meal Timing**: Automatic meal type detection (breakfast, lunch, dinner, snack)
- **Image Retrieval**: Visual representation of recommended dishes
- **Natural Language Processing**: Understand complex user preferences and dietary requirements
- **JSON Output**: Structured, machine-readable recommendations

## 📋 Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [Architecture](#architecture)
- [API Reference](#api-reference)
- [Configuration](#configuration)
- [Examples](#examples)
- [Output Format](#output-format)
- [Troubleshooting](#troubleshooting)

## 🚀 Installation

### Prerequisites

- Python 3.8+
- OpenAI API key
- SerpAPI key (for web search and image retrieval)
- Internet connection

### Dependencies

```bash
pip install requests openai python-dotenv
```

### Setup

1. Clone or download the repository

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
export OPENAI_API="your_openai_api_key"
export SERPAPI_KEY="your_serpapi_key"
```

Or create a `.env` file:
```
OPENAI_API=your_openai_api_key
SERPAPI_KEY=your_serpapi_key
```

## 🎯 Quick Start

### Basic Usage

```python
from food_planner import FoodPlanner
import json

# Initialize the planner
planner = FoodPlanner("your_serpapi_key")

# Generate a meal recommendation
user_prompt = "I want some tangy, creamy, savoury dishes in San Francisco"
recommendation = planner.generate_meal_recommendation(user_prompt)

# Display results
print(json.dumps(recommendation, indent=2))
```

### Output Example

```json
{
  "meal_type": "lunch",
  "local_time": "12:45",
  "dish": {
    "name": "Butter Chicken",
    "cuisine": "Indian",
    "description": "Delicious requested dish",
    "image_url": "https://example.com/butter_chicken.jpg"
  },
  "nutrition": {
    "calories": "350 kcal",
    "protein": "25g",
    "carbohydrates": "15g",
    "fats": "20g",
    "fiber": "2g"
  },
  "restaurants": [],
  "dietary_notes": "nonveg"
}
```

## 📖 Usage

### Simple Meal Recommendation

```python
from food_planner import FoodPlanner

planner = FoodPlanner("88e9df8bf5192113827878d7de00a1f19f57e04ff7d49e944acdd7d9a9f4a653")

# Example 1: Non-vegetarian cuisine
recommendation = planner.generate_meal_recommendation(
    "I want some tangy, creamy, savory nonveg dishes in Kharagpur"
)
print(recommendation['dish']['name'])
print(f"Calories: {recommendation['nutrition']['calories']}")
```

### With Dietary Preferences

```python
# Example 2: Vegetarian options
recommendation = planner.generate_meal_recommendation(
    "I'm vegetarian and prefer light, healthy meals. Suggest something for dinner in New York"
)

# Example 3: Vegan specific
recommendation = planner.generate_meal_recommendation(
    "I'm vegan and love Asian cuisines. I'm in Toronto and it's breakfast time"
)

# Example 4: Complex preferences
recommendation = planner.generate_meal_recommendation(
    "I'm gluten-free, non-vegetarian, love spicy food. I'm in Mumbai for lunch"
)
```

### Component-Based Usage

```python
# Use individual search methods
planner = FoodPlanner(SERPAPI_KEY)

# Search for food trends
trends = planner.search_food_trends("pad thai", "Bangkok, Thailand")
for trend in trends:
    print(f"Title: {trend['title']}")
    print(f"Snippet: {trend['snippet']}\n")

# Get nutrition information
nutrition = planner.search_nutrition_info("grilled chicken salad")
for item in nutrition:
    print(f"Title: {item['title']}")
    print(f"Info: {item['snippet']}\n")

# Find nearby restaurants
restaurants = planner.fetch_restaurants("pizza", "San Francisco, CA", "nonveg")
for restaurant in restaurants:
    print(f"Restaurant: {restaurant.get('title')}")

# Fetch dish image
image_url = planner.fetch_image("sushi roll")
print(f"Image: {image_url}")
```

## 🏗️ Architecture

### System Overview

```
User Input (Preferences, Location, Time)
    ↓
Natural Language Parser (GPT)
    ↓
Extract Preferences
├── Dietary Type (veg/nonveg/vegan)
├── Cuisine Preferences
├── Location
└── Current Time
    ↓
Recommendation Engine
├── Search Food Trends
├── Fetch Nutritional Info
├── Find Restaurants
└── Retrieve Images
    ↓
Output Formatter
    ↓
Structured JSON Recommendation
```

### Component Responsibilities

1. **NLP Parser**: Interprets user preferences using GPT
2. **Trend Analyzer**: Searches current food trends
3. **Nutrition Fetcher**: Retrieves nutritional information
4. **Restaurant Finder**: Locates nearby dining options
5. **Image Retriever**: Fetches visual representations
6. **Recommendation Engine**: Orchestrates all components

## 📚 API Reference

### FoodPlanner Class

Main class for all food planning operations.

#### Constructor

```python
FoodPlanner(serpapi_key: str)
```

**Parameters:**
- `serpapi_key`: Your SerpAPI key for web searching

#### Methods

##### `search_food_trends(dish: str, location: str = "San Francisco, CA") -> List[Dict]`

Searches for trending food items and articles related to a specific dish.

**Parameters:**
- `dish` (str): Name of the dish or cuisine to search
- `location` (str, optional): Location for context (default: "San Francisco, CA")

**Returns:**
```python
[
    {
        "title": "Best Pad Thai in San Francisco",
        "snippet": "Discover the best Thai noodle dishes...",
        "link": "https://example.com/pad-thai"
    },
    # ... more results
]
```

**Raises:**
- Prints error message if request fails; returns empty list

---

##### `search_nutrition_info(dish_name: str) -> List[Dict]`

Fetches nutritional information for a specific dish.

**Parameters:**
- `dish_name` (str): Name of the dish (e.g., "grilled chicken breast")

**Returns:**
```python
[
    {
        "title": "Grilled Chicken Breast Nutrition Facts",
        "snippet": "Calories: 165, Protein: 31g, Fat: 3.6g...",
        "link": "https://example.com/nutrition"
    },
    # ... more results
]
```

**Raises:**
- Prints error message if request fails; returns empty list

---

##### `fetch_restaurants(dish_name: str, location: str, dietary_prefs: str = None) -> List[Dict]`

Finds restaurants serving a specific dish in a given location.

**Parameters:**
- `dish_name` (str): Name of the dish (e.g., "butter chicken")
- `location` (str): Location in "City, State" format
- `dietary_prefs` (str, optional): Dietary preference (veg/nonveg/vegan)

**Returns:**
```python
[
    {
        "title": "Rajput Restaurant",
        "address": "123 Main St, San Francisco, CA",
        "rating": 4.5,
        # ... additional restaurant data
    },
    # ... more restaurants (max 3)
]
```

**Raises:**
- Prints error message if request fails; returns empty list

---

##### `fetch_image(dish_name: str) -> str`

Retrieves an image URL for a specific dish.

**Parameters:**
- `dish_name` (str): Name of the dish

**Returns:**
- String: URL to dish image, or empty string if not found

**Raises:**
- Prints error message if request fails; returns empty string

---

##### `parse_user_prompt(user_prompt: str) -> Dict`

Parses user input using GPT to extract structured meal recommendation data.

**Parameters:**
- `user_prompt` (str): Natural language user request

**Returns:**
```python
{
    "meal_type": "lunch",
    "local_time": "12:30",
    "location": "San Francisco, CA, USA",
    "dish": {
        "name": "Butter Chicken",
        "cuisine": "Indian",
        "description": "Creamy, savory chicken in tomato sauce"
    },
    "veg_nonveg": "nonveg",
    "nutrients": {
        "calories": "350 kcal",
        "protein": "25g",
        "carbohydrates": "15g",
        "fats": "20g",
        "fiber": "2g"
    },
    "dietary_type": "non-vegetarian",
    "ordering_tip": "Available on DoorDash and Uber Eats"
}
```

**Raises:**
- Returns None if GPT parsing fails

---

##### `generate_meal_recommendation(user_prompt: str) -> Dict`

Main method to generate a complete meal recommendation.

**Parameters:**
- `user_prompt` (str): Natural language request describing preferences

**Returns:**
```python
{
    "meal_type": "lunch",
    "local_time": "12:45",
    "dish": {
        "name": "Pad Thai",
        "cuisine": "Thai",
        "description": "Delicious requested dish",
        "image_url": "https://example.com/pad_thai.jpg"
    },
    "nutrition": {
        "calories": "400 kcal",
        "protein": "15g",
        "carbohydrates": "55g",
        "fats": "12g",
        "fiber": "3g"
    },
    "restaurants": [
        {
            "title": "Thai Orchid",
            "address": "456 Oak St, San Francisco",
            # ... restaurant details
        }
    ],
    "dietary_notes": "nonveg"
}
```

**Raises:**
- Handles exceptions gracefully; returns partial data if some APIs fail

## ⚙️ Configuration

### Environment Variables

```bash
# OpenAI API Key
OPENAI_API=sk-proj-xxxxxxxxxxxx

# SerpAPI Key
SERPAPI_KEY=bcbe76132dcf615504d6b69af3145f65b5ecfc43501d4e813b60c99337e44312
```

### Model Selection

The system uses GPT for parsing user preferences:

```python
MODEL_NAME = "gpt-5-mini"  # Change to gpt-4, gpt-4-turbo as needed
```

### API Rate Limiting

The system includes 2-second delays between certain API calls to avoid rate limiting:

```python
time.sleep(2)  # Between restaurant and image searches
```

Adjust if experiencing rate limit issues.

### Meal Type Detection

Meal types are automatically determined by UTC time:

```python
# 6:00 - 10:59 → Breakfast
# 11:00 - 14:59 → Lunch
# 15:00 - 20:59 → Dinner
# 21:00 - 5:59 → Snack
```

## 💡 Examples

### Example 1: Quick Lunch Recommendation

```python
from food_planner import FoodPlanner
import json

planner = FoodPlanner("your_serpapi_key")

prompt = "I'm hungry for a quick lunch in San Francisco. Non-veg, spicy preferred"
recommendation = planner.generate_meal_recommendation(prompt)

print(f"Meal: {recommendation['dish']['name']}")
print(f"Cuisine: {recommendation['dish']['cuisine']}")
print(f"Calories: {recommendation['nutrition']['calories']}")
```

### Example 2: Health-Conscious Dinner

```python
prompt = "I want a healthy, low-calorie dinner. Vegetarian. I'm in New York"
recommendation = planner.generate_meal_recommendation(prompt)

print(f"Meal Type: {recommendation['meal_type']}")
print(f"Dish: {recommendation['dish']['name']}")
print(f"Protein: {recommendation['nutrition']['protein']}")
print(f"Carbs: {recommendation['nutrition']['carbohydrates']}")
```

### Example 3: International Cuisine Discovery

```python
prompt = "Vegan breakfast option, preferably Asian cuisine, in London"
recommendation = planner.generate_meal_recommendation(prompt)

if recommendation['restaurants']:
    for restaurant in recommendation['restaurants']:
        print(f"Try: {restaurant['title']}")
```

### Example 4: Batch Recommendations

```python
user_preferences = [
    "Breakfast in Tokyo, vegetarian, light",
    "Lunch in Mumbai, nonveg, spicy",
    "Dinner in Paris, no dietary restrictions, French cuisine"
]

for pref in user_preferences:
    rec = planner.generate_meal_recommendation(pref)
    print(f"Time: {rec['local_time']} → {rec['dish']['name']}\n")
```

## 📊 Output Format

### Complete Recommendation Object

```json
{
  "meal_type": "string (breakfast/lunch/dinner/snack)",
  "local_time": "string (HH:MM)",
  "dish": {
    "name": "string",
    "cuisine": "string",
    "description": "string",
    "image_url": "string (URL)"
  },
  "nutrition": {
    "calories": "string with unit (e.g., '350 kcal')",
    "protein": "string with unit (e.g., '25g')",
    "carbohydrates": "string with unit (e.g., '45g')",
    "fats": "string with unit (e.g., '12g')",
    "fiber": "string with unit (e.g., '3g')"
  },
  "restaurants": [
    {
      "title": "string",
      "address": "string",
      "rating": "number",
      "reviews": "number"
    }
  ],
  "dietary_notes": "string or array"
}
```

## 🔐 Security Notes

- **API Keys**: Never hardcode API keys. Use environment variables
- **Rate Limiting**: SerpAPI has monthly quotas. Monitor usage
- **Data Privacy**: User preferences are processed but not stored
- **Error Handling**: Graceful degradation if external APIs fail

## 🐛 Troubleshooting

### Issue: "Invalid API Key"
**Solution**: Verify OPENAI_API and SERPAPI_KEY environment variables are correctly set

### Issue: "No restaurants found"
**Solution**: 
- Verify location format: "City, State, Country"
- Check if SerpAPI local search is available in that region
- Use more specific dish names

### Issue: "Empty nutrition data"
**Solution**:
- Ensure dish name is specific (e.g., "grilled chicken breast" not just "chicken")
- Try searching for "nutrition facts" + dish name separately

### Issue: "Rate limit exceeded"
**Solution**:
- Add longer delays between API calls
- Check your SerpAPI monthly quota
- Implement caching for repeated queries

### Issue: "No image found"
**Solution**:
- This is non-critical; recommendation still works
- Try alternative dish names
- Implement fallback placeholder image

## 📈 Performance Considerations

- **Initial recommendation**: 3-5 seconds (parsing + searches)
- **Restaurant search**: 2-3 seconds per query
- **Image retrieval**: 1-2 seconds per query
- **Total pipeline**: 5-10 seconds

### Optimization Tips

- Cache recommendations for repeated queries
- Use filters to reduce search results
- Implement asynchronous API calls
- Store frequently requested nutritional data

## 🔄 Dependencies

- `requests` - HTTP client for API calls
- `openai` - GPT API integration
- `json` - JSON parsing and serialization
- `datetime` - Time zone and time handling
- `python-dotenv` - Environment variable management
- `time` - Rate limit delays

## 📝 License

[Add your license here]

## 🤝 Support

For issues, questions, or feature requests, please contact support or open an issue in the repository.

## 🚀 Future Enhancements

- Multi-language support
- Allergy and intolerance tracking
- Macro tracking and meal planning
- Integration with food delivery apps (DoorDash, UberEats)
- Meal history and preferences learning
- Budget-based recommendations
- Seasonal ingredient preferences
- Recipe generation with instructions
- Nutritional goal optimization
- Social recommendations (what friends are eating)
- Voice input support
- Meal prep planning
- Grocery list generation
- Restaurant reservation integration

## 📚 API Resources

- [SerpAPI Documentation](https://serpapi.com)
- [OpenAI API Reference](https://platform.openai.com/docs)
- [Nutrition Database APIs](https://www.nutritionix.com/api)

---

*AI-Powered Food Planner v1.0*  
*Smart Meal Recommendations at Your Fingertips*