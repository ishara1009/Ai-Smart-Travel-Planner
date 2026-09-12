from langgraph.graph import END, START, StateGraph

from app.graph.checkpoint import checkpointer
from app.graph.nodes import (
    budget_node,
    itinerary_node,
    recommendation_node,
    search_node,
    supervisor_node,
    validator_node,
    weather_node,
)
from app.graph.routing import first_route, route_after, route_after_validator
from app.graph.state import TravelState


def build_travel_graph():
    builder = StateGraph(TravelState)
    builder.add_node("supervisor", supervisor_node)
    builder.add_node("search", search_node)
    builder.add_node("weather", weather_node)
    builder.add_node("budget", budget_node)
    builder.add_node("recommendation", recommendation_node)
    builder.add_node("itinerary", itinerary_node)
    builder.add_node("validator", validator_node)
    builder.add_edge(START, "supervisor")
    builder.add_conditional_edges("supervisor", first_route)
    for name in ("search", "weather", "budget", "recommendation", "itinerary"):
        builder.add_conditional_edges(name, route_after(name))
    builder.add_conditional_edges("validator", route_after_validator, {"itinerary": "itinerary", END: END})
    return builder.compile(checkpointer=checkpointer)


travel_graph = build_travel_graph()
