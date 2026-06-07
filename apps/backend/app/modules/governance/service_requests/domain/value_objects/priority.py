from enum import StrEnum


class Priority(StrEnum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    NORMAL = "NORMAL"
    HIGH = "HIGH"
    URGENT = "URGENT"

    def __str__(self):
        return str(self.value)
