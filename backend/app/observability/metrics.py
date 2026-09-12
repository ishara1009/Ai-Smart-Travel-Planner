from collections import Counter

REQUESTS = Counter()
AGENT_RUNS = Counter()


def snapshot() -> dict[str, dict[str, int]]:
    return {"requests": dict(REQUESTS), "agent_runs": dict(AGENT_RUNS)}
