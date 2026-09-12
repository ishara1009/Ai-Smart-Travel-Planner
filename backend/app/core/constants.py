APP_NAME = "AI Smart Travel Planner"
API_V1_PREFIX = "/api/v1"
MAX_AGENT_RETRIES = 2
MAX_QUERY_LENGTH = 2_000
DEFAULT_LLM_MODEL = "gpt-4o-mini"

AGENT_PROGRESS = {
    "supervisor": "Understanding request",
    "search": "Searching attractions",
    "weather": "Checking weather",
    "budget": "Analyzing budget",
    "recommendation": "Building recommendations",
    "itinerary": "Creating itinerary",
    "validator": "Validating plan",
}
