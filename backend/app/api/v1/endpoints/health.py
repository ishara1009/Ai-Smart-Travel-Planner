from fastapi import APIRouter, Request

router = APIRouter(tags=["Health"])


@router.get("/health")
async def health(request: Request) -> dict:
    ready = getattr(request.app.state, "database_ready", False)
    return {"status": "healthy" if ready else "degraded", "database": "connected" if ready else "unavailable"}
