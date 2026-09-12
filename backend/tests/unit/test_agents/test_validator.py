import pytest

from app.agents.validator_agent import ValidatorAgent


@pytest.mark.asyncio
async def test_validator_catches_day_count_without_llm_call():
    result = await ValidatorAgent().run({"days": 3, "itinerary": {"days": [{"day": 1}], "estimated_total": 100}, "budget_analysis": {"total_budget": 1000}})
    assert result.valid is False
    assert result.needs_replan is True
