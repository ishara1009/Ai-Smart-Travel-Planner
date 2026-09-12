import logging
import time
from contextlib import contextmanager
from collections.abc import Iterator

logger = logging.getLogger(__name__)


@contextmanager
def trace_agent(agent: str, request_id: str) -> Iterator[None]:
    started = time.perf_counter()
    logger.info("agent_started", extra={"agent": agent, "request_id": request_id})
    try:
        yield
    finally:
        logger.info(
            "agent_completed",
            extra={"agent": agent, "request_id": request_id, "duration_ms": round((time.perf_counter() - started) * 1000, 2)},
        )
