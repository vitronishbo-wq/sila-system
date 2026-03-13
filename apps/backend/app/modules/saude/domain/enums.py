from __future__ import annotations

from enum import Enum


class HealthUnitType(str, Enum):
    HEALTH_CENTER = "health_center"
    HOSPITAL = "hospital"
    CLINIC = "clinic"
    LAB = "laboratory"
    PHARMACY = "pharmacy"


class MedicationType(str, Enum):
    CONTINUOUS = "continuous"
    OCCASIONAL = "occasional"


class PrescriptionStatus(str, Enum):
    ACTIVE = "active"
    PARTIALLY_DISPENSED = "partially_dispensed"
    DISPENSED = "dispensed"
    CANCELLED = "cancelled"
    EXPIRED = "expired"


class VigilanciaStatus(str, Enum):
    REPORTED = "reported"
    INVESTIGATING = "investigating"
    CONTAINED = "contained"
    CLOSED = "closed"


__all__ = [
    "HealthUnitType",
    "MedicationType",
    "PrescriptionStatus",
    "VigilanciaStatus",
]
