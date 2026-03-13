from enum import Enum


class NationalityMode(str, Enum):
    """Nationality mode for citizen registration."""

    ANGOLAN = "angolan"
    FOREIGN = "foreign"
    UNKNOWN = "unknown"


__all__ = ["NationalityMode"]
