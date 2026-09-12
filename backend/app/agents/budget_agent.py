from app.schemas.itinerary import BudgetAnalysis
from app.tools.calculator_tool import calculate_budget


class BudgetAgent:
    name = "budget"

    async def run(self, state: dict) -> BudgetAnalysis:
        return calculate_budget(state["budget"], state["travelers"], state["days"], state["currency"])
