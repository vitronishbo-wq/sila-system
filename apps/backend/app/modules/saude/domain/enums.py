from __future__ import annotations

from enum import StrEnum


class HealthUnitType(StrEnum):
    HEALTH_CENTER = "health_center"
    HOSPITAL = "hospital"
    CLINIC = "clinic"
    LAB = "laboratory"
    PHARMACY = "pharmacy"


class MedicationType(StrEnum):
    CONTINUOUS = "continuous"
    OCCASIONAL = "occasional"


class PrescriptionStatus(StrEnum):
    ACTIVE = "active"
    PARTIALLY_DISPENSED = "partially_dispensed"
    DISPENSED = "dispensed"
    CANCELLED = "cancelled"
    EXPIRED = "expired"


class VigilanciaStatus(StrEnum):
    REPORTED = "reported"
    INVESTIGATING = "investigating"
    CONTAINED = "contained"
    CLOSED = "closed"


__all__ = ["HealthUnitType", "MedicationType", "PrescriptionStatus", "VigilanciaStatus"]
