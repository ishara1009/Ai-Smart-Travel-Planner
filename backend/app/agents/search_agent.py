from app.schemas.itinerary import SearchResult
from app.tools.tavily_tool import search_travel


class SearchAgent:
    name = "search"

    async def run(self, state: dict) -> tuple[list[str], list[SearchResult]]:
        interests = ", ".join(state.get("interests") or ["popular attractions"])
        destination = state["destination"]
        days = state.get("days", 1)
        query = (
            f"Best current nature cultural food and activity attractions in {destination} "
            f"for a {days}-day trip, interests: {interests}; official visitor information and travel notices"
        )
        return [query], await search_travel(query)
