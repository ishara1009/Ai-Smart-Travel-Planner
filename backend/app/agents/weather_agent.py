from app.schemas.itinerary import WeatherSummary
from app.tools.weather_tool import get_weather


class WeatherAgent:
    name = "weather"

    async def run(self, state: dict) -> WeatherSummary:
        return await get_weather(state["destination"])
