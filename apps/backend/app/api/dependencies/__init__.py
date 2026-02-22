"""API dependency injection layer."""

from .citizen_validation import (
    extract_citizen_id,
    extract_citizen_id_from_token,
    extract_citizen_id_from_current,
)

__all__ = [
    "extract_citizen_id",
    "extract_citizen_id_from_token",
    "extract_citizen_id_from_current",
]
