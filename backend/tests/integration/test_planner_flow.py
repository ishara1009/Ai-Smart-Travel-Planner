from datetime import date

import pytest

from app.graph.builder import travel_graph
from app.graph import nodes
from app.schemas.itinerary import (
    Activity, DayPlan, ItineraryResult, Recommendation, SearchResult, ValidationResult, WeatherSummary,
)


@pytest.mark.asyncio
async def test_mocked_full_langgraph_flow(monkeypatch):
    async def mock_search(_): return ["Kandy attractions"], [SearchResult(title="Temple", url="https://example.com/temple", content="Visitor information", score=.9)]
    async def mock_weather(_): return WeatherSummary(available=True, location="Kandy", temperature_c=26, condition="Cloudy")
    async def mock_recommendations(_): return [Recommendation(name="Temple", reason="Matches culture", category="culture", source_url="https://example.com/temple")]
    async def mock_itinerary(_): return ItineraryResult(title="Kandy in one day", summary="A grounded route", days=[DayPlan(day=1, date="2026-10-10", theme="Culture", activities=[Activity(time="09:00", title="Temple", reason="Matches culture", source_url="https://example.com/temple")], estimated_daily_cost=1000)], estimated_total=1000, currency="LKR", sources=["https://example.com/temple"])
    async def mock_validation(_): return ValidationResult(valid=True)
    monkeypatch.setattr(nodes.search, "run", mock_search)
    monkeypatch.setattr(nodes.weather, "run", mock_weather)
    monkeypatch.setattr(nodes.recommendation, "run", mock_recommendations)
    monkeypatch.setattr(nodes.itinerary, "run", mock_itinerary)
    monkeypatch.setattr(nodes.validator, "run", mock_validation)
    state = {"request_id": "test", "user_id": "user", "structured_request": True, "destination": "Kandy", "start_date": str(date(2026, 10, 10)), "days": 1, "travelers": 2, "budget": 60000, "currency": "LKR", "interests": ["culture"], "transport_preferences": ["train"], "activity_preferences": [], "retry_count": 0, "errors": [], "warnings": [], "progress": [], "status": "draft"}
    result = await travel_graph.ainvoke(state, config={"configurable": {"thread_id": "integration-test-unique"}})
    assert result["validation_result"]["valid"] is True
    assert result["status"] == "awaiting_approval"
    assert len(result["progress"]) == 7
