"""Schemas package for appointments.

This package exposes Pydantic models defined in `appointments.py` so tests and
other modules can import names from `app.modules.appointments.schemas`.
"""

from .appointments import (
    AppointmentCreate,
    AppointmentRead,
    AppointmentUpdate,
)

__all__ = [
    "AppointmentCreate",
    "AppointmentRead",
    "AppointmentUpdate",
]

__version__ = "0.1.0"
