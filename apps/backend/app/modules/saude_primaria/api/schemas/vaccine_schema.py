"""Vaccine Schemas"""
from pydantic import BaseModel, Field
from datetime import datetime, date
from typing import Optional, List
from uuid import UUID


class VaccineDoseCreateSchema(BaseModel):
    """Register vaccine dose"""
    citizen_id: UUID
    vaccine_id: UUID
    health_unit_id: UUID
    dose_number: int = Field(..., ge=1)
    batch_number: str
    application_date: date
    next_dose_date: Optional[date] = None


class VaccineDoseResponseSchema(BaseModel):
    """Vaccine dose response"""
    id: UUID
    citizen_id: UUID
    vaccine_id: UUID
    dose_number: int
    batch_number: str
    application_date: date
    next_dose_date: Optional[date]
    status: str
    has_next_dose: bool
    is_next_dose_due: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class VaccineListSchema(BaseModel):
    """Vaccine list response"""
    items: List[VaccineDoseResponseSchema]
    total: int
    skip: int
    limit: int


class VaccineDoseScheduleSchema(BaseModel):
    """Schedule next vaccine dose"""
    next_dose_date: date


class VaccineReactionSchema(BaseModel):
    """Record adverse reaction"""
    reaction: str = Field(..., min_length=5)
