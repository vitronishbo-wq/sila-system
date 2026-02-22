"""Health schemas module."""

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

# Import API schemas based on OpenAPI specification
from .api_schemas import (
    AppointmentCreate,
    AppointmentResponse,
    CancelAppointmentResponse,
    HealthRecordCreate,
    HealthRecordResponse,
    HealthRecordUpdate,
    HealthRecordsListResponse,
    HealthServiceItem,
    HealthServicesResponse,
    MedicalRecordResponse,
    UserAppointmentsResponse,
)


class HealthStatus(str, Enum):
    """Health status enumeration."""

    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING = "pending"
    COMPLETED = "completed"


class HealthBase(BaseModel):
    """Base schema for health-related entities."""

    status: HealthStatus = Field(default=HealthStatus.ACTIVE)
    notes: Optional[str] = Field(None, max_length=500)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class HealthCreate(HealthBase):
    """Schema for creating health entities."""


class HealthUpdate(BaseModel):
    """Schema for updating health entities."""

    status: Optional[HealthStatus] = None
    notes: Optional[str] = Field(None, max_length=500)


class HealthResponse(HealthBase):
    """Schema for health entity responses."""

    id: int

    model_config = ConfigDict(from_attributes=True)


class HealthInDB(HealthBase):
    """Schema for health entity in database."""

    id: int

    model_config = ConfigDict(from_attributes=True)


__all__ = [
    # Legacy schemas
    "HealthStatus",
    "HealthBase",
    "HealthCreate",
    "HealthUpdate",
    "HealthResponse",
    "HealthInDB",
    # API schemas (OpenAPI-based)
    "HealthRecordCreate",
    "HealthRecordUpdate",
    "HealthRecordResponse",
    "HealthRecordsListResponse",
    "HealthServiceItem",
    "HealthServicesResponse",
    "AppointmentCreate",
    "AppointmentResponse",
    "UserAppointmentsResponse",
    "CancelAppointmentResponse",
    "MedicalRecordResponse",
]
