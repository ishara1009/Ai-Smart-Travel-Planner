from enum import StrEnum

from pydantic import BaseModel, Field


class AgentName(StrEnum):
    SEARCH = "search"
    WEATHER = "weather"
    BUDGET = "budget"
    RECOMMENDATION = "recommendation"
    ITINERARY = "itinerary"
    VALIDATOR = "validator"


class SupervisorDecision(BaseModel):
    intent: str
    required_agents: list[AgentName]
    missing_fields: list[str] = []
    clarification_question: str | None = None
    destination: str | None = None
    start_date: str | None = None
    days: int | None = None
    travelers: int | None = None
    budget: float | None = None
    currency: str | None = None


class TravelQuery(BaseModel):
    query: str = Field(min_length=2, max_length=2000)


class TravelQueryResult(BaseModel):
    request_id: str
    intent: str
    clarification_question: str | None = None
    search_results: list[dict] = []
    weather: dict | None = None
    budget_analysis: dict | None = None
    recommendations: list[dict] = []
    itinerary: dict | None = None
    validation: dict | None = None
    warnings: list[str] = []


class AgentEvent(BaseModel):
    agent: str
    label: str
    status: str = Field(pattern="^(pending|running|completed|failed)$")
