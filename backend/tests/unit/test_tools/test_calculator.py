from app.tools.calculator_tool import calculate_budget


def test_budget_is_deterministic_and_preserves_reserve():
    result = calculate_budget(60_000, travelers=2, days=3, currency="LKR")
    assert result.estimated_total == 57_600
    assert result.remaining_budget == 2_400
    assert result.within_budget is True
    assert {item.name for item in result.categories} >= {"Accommodation", "Emergency reserve"}
