from typing import Any


def compute_score(request: dict[str, Any], reasons: list[str]) -> int:
    """Simple scoring: start at 100, subtract 10 per failed reason."""
    score = 100
    score -= 10 * len(reasons)
    return max(0, score)
