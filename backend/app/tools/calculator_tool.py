from app.schemas.itinerary import BudgetAnalysis, BudgetCategory
from app.utils.cost_utils import money


def calculate_budget(total_budget: float, travelers: int, days: int, currency: str) -> BudgetAnalysis:
    # Conservative allocation model. All figures are explicit estimates, not live prices.
    weights = {
        "Accommodation": 0.34,
        "Food": 0.20,
        "Local transport": 0.16,
        "Activities and tickets": 0.16,
        "Emergency reserve": 0.10,
    }
    categories = [
        BudgetCategory(name=name, estimated_amount=money(total_budget * weight))
        for name, weight in weights.items()
    ]
    estimated = money(sum(item.estimated_amount for item in categories))
    return BudgetAnalysis(
        total_budget=money(total_budget),
        estimated_total=estimated,
        remaining_budget=money(total_budget - estimated),
        within_budget=estimated <= total_budget,
        currency=currency,
        categories=categories,
    )
