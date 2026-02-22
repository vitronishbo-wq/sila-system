"""Pydantic schemas for justice module CRUD operations."""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field

from ..models.case import CasePriority, CaseStatus, CaseType
from ..models.case_event import EventStatus, EventType


# Base schemas
class CaseBase(BaseModel):
    """Base schema for legal cases."""

    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    case_type: CaseType
    status: CaseStatus = CaseStatus.REGISTERED
    priority: CasePriority = CasePriority.MEDIUM
    plaintiff_citizen_id: Optional[int] = None
    defendant_citizen_id: Optional[int] = None
    plaintiff_name: Optional[str] = Field(None, max_length=200)
    defendant_name: Optional[str] = Field(None, max_length=200)
    court_id: int
    judge_name: Optional[str] = Field(None, max_length=200)
    prosecutor_name: Optional[str] = Field(None, max_length=200)
    hearing_date: Optional[datetime] = None
    conclusion_date: Optional[datetime] = None
    is_public: bool = False
    is_confidential: bool = False


class CaseEventBase(BaseModel):
    """Base schema for case events."""

    case_id: int
    event_type: EventType
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    event_date: datetime
    location: Optional[str] = Field(None, max_length=200)
    judge_name: Optional[str] = Field(None, max_length=200)
    status: EventStatus = EventStatus.SCHEDULED
    is_public: bool = False


# Create schemas
class CaseCreate(CaseBase):
    """Schema for creating a case."""

    case_number: Optional[str] = Field(None, max_length=50)


class CaseEventCreate(CaseEventBase):
    """Schema for creating a case event."""


# Update schemas
class CaseUpdate(BaseModel):
    """Schema for updating a case."""

    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    status: Optional[CaseStatus] = None
    priority: Optional[CasePriority] = None
    plaintiff_citizen_id: Optional[int] = None
    defendant_citizen_id: Optional[int] = None
    plaintiff_name: Optional[str] = Field(None, max_length=200)
    defendant_name: Optional[str] = Field(None, max_length=200)
    judge_name: Optional[str] = Field(None, max_length=200)
    prosecutor_name: Optional[str] = Field(None, max_length=200)
    hearing_date: Optional[datetime] = None
    conclusion_date: Optional[datetime] = None
    is_public: Optional[bool] = None
    is_confidential: Optional[bool] = None


class CaseEventUpdate(BaseModel):
    """Schema for updating a case event."""

    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    event_date: Optional[datetime] = None
    location: Optional[str] = Field(None, max_length=200)
    judge_name: Optional[str] = Field(None, max_length=200)
    status: Optional[EventStatus] = None
    is_public: Optional[bool] = None


# Database schemas (InDB)
class CaseInDB(CaseBase):
    """Schema for case as stored in database."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    case_number: str
    filing_date: datetime
    created_by: int
    updated_by: Optional[int]
    created_at: datetime
    updated_at: datetime

    # Computed properties
    is_active: bool
    duration_days: Optional[int]


class CaseEventInDB(CaseEventBase):
    """Schema for case event as stored in database."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    created_by: int
    updated_by: Optional[int]
    created_at: datetime
    updated_at: datetime


# Output schemas (Out)
class CaseOut(CaseInDB):
    """Schema for case output (API response)."""


class CaseEventOut(CaseEventInDB):
    """Schema for case event output (API response)."""


# Filter schemas
class CaseFilter(BaseModel):
    """Schema for case filtering."""

    case_type: Optional[CaseType] = None
    status: Optional[CaseStatus] = None
    priority: Optional[CasePriority] = None
    court_id: Optional[int] = None
    created_by: Optional[int] = None
    is_active: Optional[bool] = None


class CaseEventFilter(BaseModel):
    """Schema for case event filtering."""

    case_id: Optional[int] = None
    event_type: Optional[EventType] = None
    status: Optional[EventStatus] = None
    is_public: Optional[bool] = None


# Batch operation schemas
class CaseBatchCreate(BaseModel):
    """Schema for batch creating cases."""

    cases: List[CaseCreate] = Field(..., min_items=1, max_items=100)


class CaseEventBatchCreate(BaseModel):
    """Schema for batch creating case events."""

    events: List[CaseEventCreate] = Field(..., min_items=1, max_items=100)


class CaseBatchUpdate(BaseModel):
    """Schema for batch updating cases."""

    case_ids: List[int] = Field(..., min_items=1, max_items=100)
    update_data: CaseUpdate


class CaseEventBatchUpdate(BaseModel):
    """Schema for batch updating case events."""

    event_ids: List[int] = Field(..., min_items=1, max_items=100)
    update_data: CaseEventUpdate


# Statistics schemas
class CaseStatistics(BaseModel):
    """Schema for case statistics."""

    total_cases: int
    active_cases: int
    concluded_cases: int
    pending_cases: int


class CaseEventStatistics(BaseModel):
    """Schema for case event statistics."""

    total_events: int
    completed_events: int
    scheduled_events: int
    pending_events: int
