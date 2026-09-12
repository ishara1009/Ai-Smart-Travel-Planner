import asyncio
import time
from collections import defaultdict, deque

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse


class PlannerRateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, limit: int = 10, window_seconds: int = 60):
        super().__init__(app)
        self.limit = limit
        self.window = window_seconds
        self.requests: dict[str, deque[float]] = defaultdict(deque)
        self.lock = asyncio.Lock()

    async def dispatch(self, request: Request, call_next):
        if request.method != "POST" or "/planner" not in request.url.path:
            return await call_next(request)
        client = request.client.host if request.client else "unknown"
        now = time.monotonic()
        async with self.lock:
            entries = self.requests[client]
            while entries and entries[0] <= now - self.window:
                entries.popleft()
            if len(entries) >= self.limit:
                return JSONResponse(
                    status_code=429,
                    content={"success": False, "message": "Planner rate limit exceeded", "code": "RATE_LIMITED"},
                    headers={"Retry-After": str(self.window)},
                )
            entries.append(now)
        return await call_next(request)
