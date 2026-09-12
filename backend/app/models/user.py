from datetime import datetime, timezone
from typing import Any


def new_user_document(name: str, email: str, password_hash: str) -> dict[str, Any]:
    now = datetime.now(timezone.utc)
    return {
        "name": name,
        "email": email,
        "password_hash": password_hash,
        "travel_interests": [],
        "default_currency": "LKR",
        "travel_style": None,
        "preferred_accommodation": None,
        "preferred_transport": [],
        "created_at": now,
        "updated_at": now,
    }
