import pytest

from app.core.exceptions import ExternalServiceError
from app.tools.tavily_tool import normalize_tavily_response
from app.tools.weather_tool import normalize_weatherstack_response
from app.agents.recommendation_agent import RecommendationList
from app.schemas.itinerary import ItineraryResult


def test_tavily_normalization_discards_incomplete_results():
    result = normalize_tavily_response({"results": [{"title": "Temple", "url": "https://example.com", "content": "Useful", "score": 0.9}, {"title": "Missing URL"}]})
    assert len(result) == 1
    assert result[0].title == "Temple"


def test_weatherstack_normalization_uses_actual_current_fields():
    result = normalize_weatherstack_response({"location": {"name": "Kandy"}, "current": {"temperature": 26, "weather_descriptions": ["Light rain"], "humidity": 80, "wind_speed": 9, "precip": 1.2, "observation_time": "06:00 AM"}})
    assert result.available is True
    assert result.temperature_c == 26
    assert result.precipitation_mm == 1.2
    assert "Current conditions only" in result.limitation


def test_weatherstack_error_is_not_hallucinated():
    with pytest.raises(ExternalServiceError):
        normalize_weatherstack_response({"success": False, "error": {"info": "bad key"}})


def test_llm_output_schemas_do_not_emit_unsupported_uri_format():
    schemas = [RecommendationList.model_json_schema(), ItineraryResult.model_json_schema()]

    def contains_uri_format(value):
        if isinstance(value, dict):
            return value.get("format") == "uri" or any(contains_uri_format(item) for item in value.values())
        if isinstance(value, list):
            return any(contains_uri_format(item) for item in value)
        return False

    assert not any(contains_uri_format(schema) for schema in schemas)
