"""Exam Request Schemas"""
from pydantic import BaseModel, Field
from datetime import datetime, date
from typing import Optional
from uuid import UUID


class ExamRequestCreateSchema(BaseModel):
    """Create exam request"""
    citizen_id: UUID
    doctor_id: UUID
    health_unit_id: UUID
    exam_type: str = Field(..., min_length=2)
    exam_description: str = Field(..., min_length=10)
    clinical_indication: str = Field(..., min_length=10)
    priority: str = "MEDIA"


class ExamRequestResponseSchema(BaseModel):
    """Exam request response"""
    id: UUID
    request_number: Optional[str]
    citizen_id: UUID
    doctor_id: UUID
    health_unit_id: UUID
    exam_type: str
    exam_description: str
    clinical_indication: str
    status: str
    priority: str
    requested_date: date
    scheduled_date: Optional[date]
    collection_date: Optional[date]
    result_date: Optional[date]
    result_file: Optional[str]
    result_notes: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class ExamRequestScheduleSchema(BaseModel):
    """Schedule exam"""
    scheduled_date: date


class ExamRequestCollectSchema(BaseModel):
    """Collect exam sample"""
    pass


class ExamRequestCompleteSchema(BaseModel):
    """Complete exam"""
    result_notes: str = Field(..., min_length=5)
    result_file: Optional[str] = None


class ExamRequestCancelSchema(BaseModel):
    """Cancel exam"""
    reason: str = Field(..., min_length=5)
