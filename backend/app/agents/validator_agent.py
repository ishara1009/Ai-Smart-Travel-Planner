import json

from app.prompts.validator import VALIDATOR_PROMPT
from app.schemas.itinerary import ValidationResult
from app.tools.llm_tool import structured_completion


class ValidatorAgent:
    name = "validator"

    async def run(self, state: dict) -> ValidationResult:
        itinerary = state.get("itinerary") or {}
        deterministic_errors: list[str] = []
        if len(itinerary.get("days", [])) != state.get("days"):
            deterministic_errors.append("The itinerary day count does not match the request.")
        budget = state.get("budget_analysis") or {}
        if itinerary.get("estimated_total", 0) > budget.get("total_budget", float("inf")):
            deterministic_errors.append("The itinerary exceeds the total budget.")
        if deterministic_errors:
            return ValidationResult(valid=False, errors=deterministic_errors, needs_replan=True)
        return await structured_completion(
            ValidationResult,
            VALIDATOR_PROMPT,
            json.dumps(
                {
                    "request": {key: state.get(key) for key in ("destination", "start_date", "days", "interests")},
                    "search_results": state.get("search_results", []),
                    "weather": state.get("weather_data"),
                    "budget": budget,
                    "itinerary": itinerary,
                    "upstream_errors": state.get("errors", []),
                },
                default=str,
            ),
        )
