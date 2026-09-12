from datetime import datetime, timezone
from typing import Any

from bson import ObjectId


def conversation_document(trip_id: str, role: str, content: str) -> dict[str, Any]:
    return {
        "trip_id": ObjectId(trip_id),
        "role": role,
        "content": content,
        "created_at": datetime.now(timezone.utc),
    }
