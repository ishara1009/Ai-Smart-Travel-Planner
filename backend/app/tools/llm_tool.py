from functools import lru_cache
from typing import TypeVar

from langchain_openai import ChatOpenAI
from pydantic import BaseModel

from app.core.config import get_settings
from app.core.exceptions import ExternalServiceError

T = TypeVar("T", bound=BaseModel)


@lru_cache
def get_llm() -> ChatOpenAI:
    settings = get_settings()
    if not settings.openai_api_key:
        raise ExternalServiceError("openai", "OpenAI is not configured")
    return ChatOpenAI(
        api_key=settings.openai_api_key,
        model=settings.openai_model,
        temperature=0.2,
        timeout=settings.external_api_timeout_seconds,
        max_retries=2,
    )


async def structured_completion(schema: type[T], system_prompt: str, payload: str) -> T:
    try:
        structured_llm = get_llm().with_structured_output(schema, method="json_schema")
        result = await structured_llm.ainvoke(
            [("system", system_prompt), ("human", payload)]
        )
        if not isinstance(result, schema):
            return schema.model_validate(result)
        return result
    except ExternalServiceError:
        raise
    except Exception as exc:
        raise ExternalServiceError("openai", "AI planning is temporarily unavailable") from exc
