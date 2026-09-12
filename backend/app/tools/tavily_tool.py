import asyncio

from tavily import AsyncTavilyClient

from app.core.config import get_settings
from app.core.exceptions import ExternalServiceError
from app.schemas.itinerary import SearchResult
from app.utils.text_utils import compact_text


def normalize_tavily_response(payload: dict) -> list[SearchResult]:
    normalized: list[SearchResult] = []
    for item in payload.get("results", []):
        if not item.get("title") or not item.get("url"):
            continue
        normalized.append(
            SearchResult(
                title=compact_text(str(item["title"]), 200),
                url=item["url"],
                content=compact_text(str(item.get("content", "")), 1200),
                score=item.get("score"),
            )
        )
    return normalized


async def search_travel(query: str, max_results: int = 8) -> list[SearchResult]:
    settings = get_settings()
    if not settings.tavily_api_key:
        raise ExternalServiceError("tavily", "Live travel search is not configured")
    client = AsyncTavilyClient(api_key=settings.tavily_api_key)
    try:
        payload = await asyncio.wait_for(
            client.search(
                query=query,
                search_depth="basic",
                topic="general",
                max_results=max_results,
                include_answer=False,
                include_raw_content=False,
            ),
            timeout=settings.external_api_timeout_seconds,
        )
        return normalize_tavily_response(payload)
    except Exception as exc:
        raise ExternalServiceError("tavily", "Live travel information is temporarily unavailable") from exc
