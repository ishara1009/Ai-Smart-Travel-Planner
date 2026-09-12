from typing import Literal

from langgraph.graph import END

from app.core.constants import MAX_AGENT_RETRIES

AgentRoute = Literal["search", "weather", "budget", "recommendation", "itinerary", "validator", "__end__"]
ORDER = ["search", "weather", "budget", "recommendation", "itinerary", "validator"]


def first_route(state: dict) -> AgentRoute:
    decision = state.get("supervisor_decision", {})
    if decision.get("missing_fields"):
        return END
    required = decision.get("required_agents", [])
    return next((name for name in ORDER if name in required), END)


def route_after(current: str):
    def route(state: dict) -> AgentRoute:
        required = state.get("supervisor_decision", {}).get("required_agents", [])
        start = ORDER.index(current) + 1
        return next((name for name in ORDER[start:] if name in required), END)

    return route


def route_after_validator(state: dict) -> Literal["itinerary", "__end__"]:
    validation = state.get("validation_result") or {}
    if validation.get("needs_replan") and state.get("retry_count", 0) < MAX_AGENT_RETRIES:
        return "itinerary"
    return END
