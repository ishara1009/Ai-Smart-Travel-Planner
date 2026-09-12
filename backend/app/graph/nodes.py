from app.agents.budget_agent import BudgetAgent
from app.agents.itinerary_agent import ItineraryAgent
from app.agents.recommendation_agent import RecommendationAgent
from app.agents.search_agent import SearchAgent
from app.agents.supervisor_agent import SupervisorAgent
from app.agents.validator_agent import ValidatorAgent
from app.agents.weather_agent import WeatherAgent
from app.core.constants import AGENT_PROGRESS
from app.core.exceptions import ExternalServiceError

supervisor = SupervisorAgent()
search = SearchAgent()
weather = WeatherAgent()
budget = BudgetAgent()
recommendation = RecommendationAgent()
itinerary = ItineraryAgent()
validator = ValidatorAgent()


def event(agent: str, status: str = "completed") -> list[dict[str, str]]:
    return [{"agent": agent, "label": AGENT_PROGRESS[agent], "status": status}]


async def supervisor_node(state: dict) -> dict:
    result = await supervisor.run(state)
    updates = {"supervisor_decision": result.model_dump(mode="json"), "progress": event("supervisor")}
    for key in ("destination", "start_date", "days", "travelers", "budget", "currency"):
        value = getattr(result, key, None)
        if not state.get(key) and value is not None:
            updates[key] = value
    return updates


async def search_node(state: dict) -> dict:
    try:
        queries, results = await search.run(state)
        return {
            "search_queries": queries,
            "search_results": [item.model_dump(mode="json") for item in results],
            "progress": event("search"),
        }
    except ExternalServiceError as exc:
        return {
            "search_results": [],
            "errors": [exc.message],
            "warnings": ["Recommendations may be limited because live web information is unavailable."],
            "progress": event("search", "failed"),
        }


async def weather_node(state: dict) -> dict:
    try:
        result = await weather.run(state)
        return {"weather_data": result.model_dump(mode="json"), "progress": event("weather")}
    except ExternalServiceError as exc:
        return {
            "weather_data": {"available": False, "limitation": exc.message},
            "errors": [exc.message],
            "warnings": ["Weather could not be verified; check a forecast before travel."],
            "progress": event("weather", "failed"),
        }


async def budget_node(state: dict) -> dict:
    result = await budget.run(state)
    return {"budget_analysis": result.model_dump(mode="json"), "progress": event("budget")}


async def recommendation_node(state: dict) -> dict:
    results = await recommendation.run(state)
    return {"recommendations": [item.model_dump(mode="json") for item in results], "progress": event("recommendation")}


async def itinerary_node(state: dict) -> dict:
    result = await itinerary.run(state)
    return {
        "itinerary": result.model_dump(mode="json"),
        "retry_count": state.get("retry_count", 0) + (1 if state.get("validation_result") else 0),
        "progress": event("itinerary"),
    }


async def validator_node(state: dict) -> dict:
    result = await validator.run(state)
    return {
        "validation_result": result.model_dump(mode="json"),
        "warnings": result.warnings,
        "status": "awaiting_approval" if result.valid else "failed",
        "progress": event("validator"),
    }
