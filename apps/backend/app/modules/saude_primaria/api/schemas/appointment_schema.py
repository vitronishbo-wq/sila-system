"""Appointment Schemas"""
from pydantic import BaseModel, Field, field_validator
from datetime import datetime, date, time
from typing import Optional, List
from uuid import UUID


class AppointmentCreateSchema(BaseModel):
    """Create appointment"""
    citizen_id: UUID
    health_unit_id: UUID
    appointment_type: str = Field(..., min_length=1)
    specialty: str = Field(..., min_length=2)
    appointment_date: date
    appointment_time: time
    reason: str = Field(..., min_length=5)
    priority: str = "MEDIA"
    doctor_id: Optional[UUID] = None
    symptoms: Optional[str] = None
    notes: Optional[str] = None
    
    @field_validator("appointment_type")
    @classmethod
    def validate_appointment_type(cls, v):
        valid_types = ["ROTINA", "URGENCIA", "EMERGENCIA", "RETORNO", "ESPECIALIDADE", "PREVENTIVA"]
        if v not in valid_types:
            raise ValueError(f"Invalid appointment type: {v}")
        return v


class AppointmentResponseSchema(BaseModel):
    """Appointment response"""
    id: UUID
    appointment_number: Optional[str]
    citizen_id: UUID
    created_by: UUID
    doctor_id: Optional[UUID]
    health_unit_id: UUID
    appointment_type: str
    specialty: str
    appointment_date: date
    appointment_time: time
    status: str
    priority: str
    reason: str
    symptoms: Optional[str]
    notes: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]
    confirmed_at: Optional[datetime]
    completed_at: Optional[datetime]
    cancelled_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class AppointmentListSchema(BaseModel):
    """Appointment list response"""
    items: List[AppointmentResponseSchema]
    total: int
    skip: int
    limit: int


class AppointmentConfirmSchema(BaseModel):
    """Confirm appointment"""
    pass


class AppointmentCancelSchema(BaseModel):
    """Cancel appointment"""
    reason: str = Field(..., min_length=5)


class AppointmentRescheduleSchema(BaseModel):
    """Reschedule appointment"""
    new_date: date
    new_time: time


class AppointmentAssignSchema(BaseModel):
    """Assign doctor to appointment"""
    doctor_id: UUID
