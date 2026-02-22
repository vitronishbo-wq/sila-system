from enum import Enum


class Priority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    NORMAL = "NORMAL"
    HIGH = "HIGH"
    URGENT = "URGENT"

    def __str__(self):
        return str(self.value)
