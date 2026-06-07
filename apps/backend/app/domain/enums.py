from __future__ import annotations

from enum import StrEnum


class CitizenStatus(StrEnum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    DECEASED = "deceased"


class Gender(StrEnum):
    M = "M"
    F = "F"
    O = "O"
    U = "U"


class MaritalStatus(StrEnum):
    SINGLE = "single"
    MARRIED = "married"
    DIVORCED = "divorced"
    WIDOWED = "widowed"


# Backwards-compatible aliases expected by presentation layer
CitizenStatusEnum = CitizenStatus
GenderEnum = Gender
MaritalStatusEnum = MaritalStatus


__all__ = [
    "CitizenStatus",
    "Gender",
    "MaritalStatus",
    "CitizenStatusEnum",
    "GenderEnum",
    "MaritalStatusEnum",
]
