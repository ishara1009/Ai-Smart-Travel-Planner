import operator
from typing import Annotated, Any, TypedDict


class TravelState(TypedDict, total=False):
    request_id: str
    user_id: str
    user_query: str
    structured_request: bool
    destination: str
    start_date: str
    days: int
    travelers: int
    budget: float
    currency: str
    interests: list[str]
    transport_preferences: list[str]
    accommodation_preference: str | None
    food_preference: str | None
    activity_preferences: list[str]
    special_requirements: str | None
    modification_instructions: str | None
    previous_itinerary: dict[str, Any] | None
    supervisor_decision: dict[str, Any]
    search_queries: list[str]
    search_results: list[dict[str, Any]]
    weather_data: dict[str, Any] | None
    budget_analysis: dict[str, Any] | None
    recommendations: list[dict[str, Any]]
    itinerary: dict[str, Any] | None
    validation_result: dict[str, Any] | None
    retry_count: int
    errors: Annotated[list[str], operator.add]
    warnings: Annotated[list[str], operator.add]
    progress: Annotated[list[dict[str, str]], operator.add]
    status: str
