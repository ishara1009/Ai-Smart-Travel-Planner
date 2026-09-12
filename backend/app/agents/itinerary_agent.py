import json

from app.prompts.itinerary import ITINERARY_PROMPT
from app.schemas.itinerary import ItineraryResult
from app.tools.llm_tool import structured_completion


class ItineraryAgent:
    name = "itinerary"

    async def run(self, state: dict) -> ItineraryResult:
        payload = {
            "destination": state.get("destination"),
            "start_date": state.get("start_date"),
            "days": state.get("days"),
            "travelers": state.get("travelers"),
            "currency": state.get("currency"),
            "preferences": {
                "interests": state.get("interests", []),
                "transport": state.get("transport_preferences", []),
                "accommodation": state.get("accommodation_preference"),
                "food": state.get("food_preference"),
                "activities": state.get("activity_preferences", []),
                "requirements": state.get("special_requirements"),
            },
            "search_results": state.get("search_results", []),
            "weather": state.get("weather_data"),
            "budget": state.get("budget_analysis"),
            "recommendations": state.get("recommendations", []),
            "modification_instructions": state.get("modification_instructions"),
            "previous_itinerary": state.get("previous_itinerary"),
            "validation_errors": state.get("validation_result", {}).get("errors", []),
        }
        return await structured_completion(ItineraryResult, ITINERARY_PROMPT, json.dumps(payload, default=str))
