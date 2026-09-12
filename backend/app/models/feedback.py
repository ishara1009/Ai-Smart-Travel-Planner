from datetime import datetime, timezone
from typing import Any

from bson import ObjectId


def feedback_document(trip_id: str, user_id: str, rating: int, comment: str | None) -> dict[str, Any]:
    return {
        "trip_id": ObjectId(trip_id),
        "user_id": ObjectId(user_id),
        "rating": rating,
        "comment": comment,
        "created_at": datetime.now(timezone.utc),
    }
