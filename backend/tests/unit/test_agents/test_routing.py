from langgraph.graph import END

from app.graph.routing import first_route, route_after


def test_weather_only_routes_to_weather_then_end():
    state = {"supervisor_decision": {"required_agents": ["weather"]}}
    assert first_route(state) == "weather"
    assert route_after("weather")(state) == END


def test_missing_information_stops_for_clarification():
    state = {"supervisor_decision": {"required_agents": ["weather"], "missing_fields": ["destination"]}}
    assert first_route(state) == END


def test_full_plan_follows_declared_agent_order():
    state = {"supervisor_decision": {"required_agents": ["search", "weather", "budget", "recommendation", "itinerary", "validator"]}}
    assert first_route(state) == "search"
    assert route_after("search")(state) == "weather"
    assert route_after("budget")(state) == "recommendation"
