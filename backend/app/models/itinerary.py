from datetime import datetime, timezone
from typing import Any

from bson import ObjectId


def itinerary_document(trip_id: str, payload: dict[str, Any]) -> dict[str, Any]:
    now = datetime.now(timezone.utc)
    return {"trip_id": ObjectId(trip_id), "payload": payload, "updated_at": now}
