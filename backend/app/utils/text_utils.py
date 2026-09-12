def compact_text(value: str, limit: int = 1000) -> str:
    return " ".join(value.split())[:limit]
