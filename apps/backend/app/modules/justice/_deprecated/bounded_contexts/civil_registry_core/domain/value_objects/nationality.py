from enum import Enum, StrEnum


class NationalityMode(StrEnum):
    """Nationality mode for citizen registration."""

    ANGOLAN = "angolan"
    FOREIGN = "foreign"
    UNKNOWN = "unknown"


__all__ = ["NationalityMode"]
