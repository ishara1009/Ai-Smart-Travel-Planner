import httpx

from app.core.config import get_settings
from app.core.exceptions import ExternalServiceError
from app.schemas.itinerary import WeatherSummary

WEATHERSTACK_URL = "https://api.weatherstack.com/current"


def normalize_weatherstack_response(payload: dict) -> WeatherSummary:
    if payload.get("success") is False or "error" in payload:
        message = payload.get("error", {}).get("info", "Weatherstack returned an error")
        raise ExternalServiceError("weather", message)
    location = payload.get("location") or {}
    current = payload.get("current") or {}
    descriptions = current.get("weather_descriptions") or []
    return WeatherSummary(
        available=bool(current),
        location=location.get("name"),
        observed_at=current.get("observation_time"),
        temperature_c=current.get("temperature"),
        condition=descriptions[0] if descriptions else None,
        humidity=current.get("humidity"),
        wind_kph=current.get("wind_speed"),
        precipitation_mm=current.get("precip"),
        limitation=(
            "Current conditions only. The configured endpoint does not provide a future forecast; "
            "verify conditions again before travel."
        ),
    )


async def get_weather(destination: str) -> WeatherSummary:
    settings = get_settings()
    if not settings.weatherstack_api_key:
        raise ExternalServiceError("weather", "Weatherstack is not configured")
    try:
        async with httpx.AsyncClient(timeout=settings.external_api_timeout_seconds) as client:
            response = await client.get(
                WEATHERSTACK_URL,
                params={"access_key": settings.weatherstack_api_key, "query": destination, "units": "m"},
            )
            response.raise_for_status()
        return normalize_weatherstack_response(response.json())
    except ExternalServiceError:
        raise
    except (httpx.HTTPError, ValueError) as exc:
        raise ExternalServiceError("weather") from exc
