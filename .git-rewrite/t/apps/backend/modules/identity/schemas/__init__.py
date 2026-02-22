"""
Identity module schemas.

This module contains Pydantic schemas for the identity module,
including validation and serialization schemas.
"""

from .citizen_identity import (
    CitizenIdentityBase,
    CitizenIdentityCreate,
    CitizenIdentityRead,
    CitizenIdentityUpdate,
    CitizenIdentityWithRelations,
    GenderEnum,
)

from .identity import (
    IdentityBase,
    IdentityCreate,
    IdentityRead,
    IdentityUpdate,
    IdentityWithUser,
    IdentityList,
)

__all__ = [
    # Citizen Identity schemas
    "CitizenIdentityBase",
    "CitizenIdentityCreate",
    "CitizenIdentityUpdate",
    "CitizenIdentityRead",
    "CitizenIdentityWithRelations",
    "GenderEnum",
    # Identity schemas
    "IdentityBase",
    "IdentityCreate",
    "IdentityUpdate",
    "IdentityRead",
    "IdentityWithUser",
    "IdentityList",
]
