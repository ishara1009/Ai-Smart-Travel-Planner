import json

from pydantic import BaseModel

from app.prompts.recommendation import RECOMMENDATION_PROMPT
from app.schemas.itinerary import Recommendation
from app.tools.llm_tool import structured_completion


class RecommendationList(BaseModel):
    recommendations: list[Recommendation]


class RecommendationAgent:
    name = "recommendation"

    async def run(self, state: dict) -> list[Recommendation]:
        result = await structured_completion(
            RecommendationList,
            RECOMMENDATION_PROMPT,
            json.dumps(
                {
                    "destination": state.get("destination"),
                    "interests": state.get("interests", []),
                    "search_results": state.get("search_results", []),
                    "weather": state.get("weather_data"),
                    "budget": state.get("budget_analysis"),
                },
                default=str,
            ),
        )
        return result.recommendations
