from datetime import datetime, timezone
from typing import Any

from bson import ObjectId

from app.schemas.trip import TravelRequest, TripStatus


def new_trip_document(user_id: str, request: TravelRequest) -> dict[str, Any]:
    now = datetime.now(timezone.utc)
    return {
        "user_id": ObjectId(user_id),
        **request.model_dump(mode="json"),
        "status": TripStatus.DRAFT.value,
        "weather": None,
        "budget_analysis": None,
        "recommendations": [],
        "itinerary": None,
        "warnings": [],
        "created_at": now,
        "updated_at": now,
    }
