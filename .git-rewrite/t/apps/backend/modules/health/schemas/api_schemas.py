"""
Health module API schemas based on OpenAPI specification.

These schemas are used for Health module endpoints and follow the OpenAPI contract.
"""

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import Field, ConfigDict

from modules.common.bases.bases import BaseSchema

# ============================================================================
# Health Record Schemas
# ============================================================================


class HealthRecordCreate(BaseSchema):
    """Schema for creating a health record."""

    patient_name: Optional[str] = Field(None, description="Patient name")
    diagnosis: Optional[str] = Field(None, description="Diagnosis")
    notes: Optional[str] = Field(None, description="Additional notes")


class HealthRecordUpdate(BaseSchema):
    """Schema for updating a health record."""

    patient_name: Optional[str] = Field(None, description="Patient name")
    diagnosis: Optional[str] = Field(None, description="Diagnosis")
    notes: Optional[str] = Field(None, description="Additional notes")


class HealthRecordResponse(BaseSchema):
    """Schema for health record response."""

    id: UUID = Field(..., description="Record unique identifier")
    patient_name: Optional[str] = Field(None, description="Patient name")
    diagnosis: Optional[str] = Field(None, description="Diagnosis")
    notes: Optional[str] = Field(None, description="Additional notes")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")


class HealthRecordsListResponse(BaseSchema):
    """Schema for list of health records response."""

    items: List[HealthRecordResponse] = Field(
        default_factory=list, description="List of health records"
    )
    total: int = Field(
        ..., description="Total number of records", json_schema_extra={"example": 0}
    )


# ============================================================================
# Health Service Schemas
# ============================================================================


class HealthServiceItem(BaseSchema):
    """Schema for a single health service item."""

    id: str = Field(..., description="Service identifier")
    name: str = Field(..., description="Service name")
    category: Optional[str] = Field(None, description="Service category")
    status: Optional[str] = Field(None, description="Service status")


class HealthServicesResponse(BaseSchema):
    """Schema for health services response."""

    services: List[HealthServiceItem] = Field(
        default_factory=list, description="List of health services"
    )
    total: int = Field(
        ..., description="Total number of services", json_schema_extra={"example": 0}
    )


# ============================================================================
# Appointment Schemas
# ============================================================================


class AppointmentCreate(BaseSchema):
    """Schema for creating an appointment."""

    service_id: str = Field(..., description="Service identifier")
    scheduled_date: datetime = Field(..., description="Scheduled date and time")
    notes: Optional[str] = Field(None, description="Additional notes")


class AppointmentResponse(BaseSchema):
    """Schema for appointment response."""

    id: str = Field(..., description="Appointment identifier")
    service_id: str = Field(..., description="Service identifier")
    scheduled_date: datetime = Field(..., description="Scheduled date and time")
    notes: Optional[str] = Field(None, description="Additional notes")
    status: Optional[str] = Field(None, description="Appointment status")
    created_at: datetime = Field(..., description="Creation timestamp")


class UserAppointmentsResponse(BaseSchema):
    """Schema for user appointments response."""

    appointments: List[AppointmentResponse] = Field(
        default_factory=list, description="List of appointments"
    )
    total: int = Field(
        ...,
        description="Total number of appointments",
        json_schema_extra={"example": 0},
    )


class CancelAppointmentResponse(BaseSchema):
    """Schema for cancel appointment response."""

    message: str = Field(
        ...,
        description="Response message",
        json_schema_extra={"example": "Appointment cancelled successfully"},
    )
    appointment_id: str = Field(..., description="Cancelled appointment identifier")


# ============================================================================
# Medical Record Schemas
# ============================================================================


class MedicalRecordResponse(BaseSchema):
    """Schema for medical record response."""

    id: str = Field(..., description="Medical record identifier")
    appointment_id: str = Field(..., description="Related appointment identifier")
    diagnosis: Optional[str] = Field(None, description="Diagnosis")
    treatment: Optional[str] = Field(None, description="Treatment")
    notes: Optional[str] = Field(None, description="Additional notes")
    created_at: datetime = Field(..., description="Creation timestamp")


# ============================================================================
# Health Status Schemas
# ============================================================================


class HealthStatusResponse(BaseSchema):
    """Schema for health status response."""

    status: str = Field(..., description="Health status")
    timestamp: datetime = Field(..., description="Check timestamp")
    details: Optional[dict] = Field(None, description="Additional details")


class ServiceHealthResponse(BaseSchema):
    """Schema for service health response."""

    service: str = Field(..., description="Service name")
    status: str = Field(..., description="Service status")
    response_time: Optional[float] = Field(None, description="Response time in ms")
    last_checked: datetime = Field(..., description="Last health check")


class HealthMetricsResponse(BaseSchema):
    """Schema for health metrics response."""

    total_patients: int = Field(0, description="Total number of patients")
    active_appointments: int = Field(0, description="Active appointments count")
    available_services: int = Field(0, description="Available services count")
    system_uptime: float = Field(0.0, description="System uptime percentage")


__all__ = [
    # Health Record
    "HealthRecordCreate",
    "HealthRecordUpdate",
    "HealthRecordResponse",
    "HealthRecordsListResponse",
    # Health Services
    "HealthServiceItem",
    "HealthServicesResponse",
    # Appointments
    "AppointmentCreate",
    "AppointmentResponse",
    "UserAppointmentsResponse",
    "CancelAppointmentResponse",
    # Medical Records
    "MedicalRecordResponse",
    # Health Status
    "HealthStatusResponse",
    "ServiceHealthResponse",
    "HealthMetricsResponse",
]
