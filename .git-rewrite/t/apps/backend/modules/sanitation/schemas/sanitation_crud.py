"""Pydantic schemas for sanitation module with CRUD support."""

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, validator


# Base schemas
class SanitationBase(BaseModel):
    """Base schema for sanitation records."""

    municipality_id: int
    sanitation_type: str = Field(..., description="Type of sanitation service")
    coverage_percentage: float = Field(
        ..., ge=0, le=100, description="Coverage percentage"
    )
    responsible_entity: Optional[str] = Field(
        None, description="Entity responsible for service"
    )
    technical_manager: Optional[str] = Field(None, description="Technical manager name")

    @validator("sanitation_type")
    def validate_sanitation_type(cls, v):
        allowed_types = ["WATER", "SEWAGE", "WASTE", "HYGIENE"]
        if v.upper() not in allowed_types:
            raise ValueError(f"Sanitation type must be one of: {allowed_types}")
        return v.upper()


# CRUD operation schemas
class SanitationCreate(SanitationBase):
    """Schema for creating sanitation records."""


class SanitationUpdate(BaseModel):
    """Schema for updating sanitation records."""

    municipality_id: Optional[int] = None
    sanitation_type: Optional[str] = None
    coverage_percentage: Optional[float] = Field(None, ge=0, le=100)
    responsible_entity: Optional[str] = None
    technical_manager: Optional[str] = None

    @validator("sanitation_type")
    def validate_sanitation_type(cls, v):
        if v is not None:
            allowed_types = ["WATER", "SEWAGE", "WASTE", "HYGIENE"]
            if v.upper() not in allowed_types:
                raise ValueError(f"Sanitation type must be one of: {allowed_types}")
            return v.upper()
        return v


class SanitationInDB(SanitationBase):
    """Schema for sanitation records as stored in database."""

    id: int
    last_updated: datetime

    class Config:
        from_attributes = True


class SanitationOut(SanitationInDB):
    """Schema for sanitation records output."""


# Filter schemas for advanced queries
class SanitationFilter(BaseModel):
    """Schema for filtering sanitation records."""

    municipality_id: Optional[int] = None
    sanitation_type: Optional[str] = None
    responsible_entity: Optional[str] = None
    technical_manager: Optional[str] = None
    min_coverage: Optional[float] = Field(None, ge=0, le=100)
    max_coverage: Optional[float] = Field(None, ge=0, le=100)
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    skip: Optional[int] = Field(0, ge=0)
    limit: Optional[int] = Field(100, ge=1, le=1000)


# Statistics schemas
class SanitationStatistics(BaseModel):
    """Schema for sanitation statistics."""

    total_records: int
    avg_coverage: float
    min_coverage: float
    max_coverage: float
    by_type: Dict[str, Dict[str, Any]] = Field(default_factory=dict)
    last_updated: Optional[datetime] = None


class SanitationTypeBreakdown(BaseModel):
    """Schema for sanitation type breakdown."""

    type: str
    count: int
    avg_coverage: float
    total_records: int


# Batch operation schemas
class SanitationBatchCreate(BaseModel):
    """Schema for batch creating sanitation records."""

    records: List[SanitationCreate] = Field(..., min_items=1, max_items=100)


class SanitationBatchUpdate(BaseModel):
    """Schema for batch updating sanitation records."""

    updates: List[Dict[str, Any]] = Field(..., min_items=1, max_items=100)


class SanitationBatchDelete(BaseModel):
    """Schema for batch deleting sanitation records."""

    ids: List[int] = Field(..., min_items=1, max_items=100)


# Response schemas
class SanitationListResponse(BaseModel):
    """Schema for list response with pagination."""

    items: List[SanitationOut]
    total: int
    skip: int
    limit: int
    has_next: bool
    has_prev: bool


class SanitationBatchResponse(BaseModel):
    """Schema for batch operation response."""

    successful: List[SanitationOut]
    failed: List[Dict[str, Any]]
    total_attempted: int
    total_successful: int
    total_failed: int


# Legacy schemas for backward compatibility
class IncidentCreate(BaseModel):
    """Legacy schema for incident creation."""

    title: str
    description: str
    location: str
    severity: str = Field(..., regex="^(LOW|MEDIUM|HIGH|CRITICAL)$")
    reported_by: str
    contact_phone: Optional[str] = None


class IncidentUpdate(BaseModel):
    """Legacy schema for incident update."""

    title: Optional[str] = None
    description: Optional[str] = None
    severity: Optional[str] = Field(None, regex="^(LOW|MEDIUM|HIGH|CRITICAL)$")
    status: Optional[str] = Field(None, regex="^(OPEN|IN_PROGRESS|RESOLVED|CLOSED)$")


class IncidentOut(BaseModel):
    """Legacy schema for incident output."""

    id: int
    title: str
    description: str
    location: str
    severity: str
    status: str
    reported_by: str
    contact_phone: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Technician schemas
class TechnicianBase(BaseModel):
    """Base schema for technician."""

    name: str
    email: str
    phone: Optional[str] = None
    specialization: str
    is_active: bool = True


class TechnicianCreate(TechnicianBase):
    """Schema for creating technician."""


class TechnicianUpdate(BaseModel):
    """Schema for updating technician."""

    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    specialization: Optional[str] = None
    is_active: Optional[bool] = None


class TechnicianOut(TechnicianBase):
    """Schema for technician output."""

    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Utility schemas
class Placeholder(BaseModel):
    """Placeholder schema for future use."""


# Export all schemas
__all__ = [
    # Base schemas
    "SanitationBase",
    "SanitationCreate",
    "SanitationUpdate",
    "SanitationInDB",
    "SanitationOut",
    # Filter schemas
    "SanitationFilter",
    # Statistics schemas
    "SanitationStatistics",
    "SanitationTypeBreakdown",
    # Batch operation schemas
    "SanitationBatchCreate",
    "SanitationBatchUpdate",
    "SanitationBatchDelete",
    # Response schemas
    "SanitationListResponse",
    "SanitationBatchResponse",
    # Legacy schemas
    "IncidentCreate",
    "IncidentUpdate",
    "IncidentOut",
    # Technician schemas
    "TechnicianBase",
    "TechnicianCreate",
    "TechnicianUpdate",
    "TechnicianOut",
    # Utility schemas
    "Placeholder",
]
