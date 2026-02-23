"""Prescription Schemas"""
from pydantic import BaseModel, Field
from datetime import datetime, date
from typing import Optional, List
from uuid import UUID


class PrescriptionItemSchema(BaseModel):
    """Prescription item"""
    medication_code: str
    medication_name: str
    dosage: str
    frequency: str
    duration_days: int
    quantity: int
    unit: str
    notes: Optional[str] = None
    medication_type: str = "USO_OCASIONAL"


class PrescriptionCreateSchema(BaseModel):
    """Create prescription"""
    citizen_id: UUID
    doctor_id: UUID
    health_unit_id: UUID
    items: List[PrescriptionItemSchema]
    appointment_id: Optional[UUID] = None
    clinical_notes: Optional[str] = None
    recommendations: Optional[str] = None


class PrescriptionResponseSchema(BaseModel):
    """Prescription response"""
    id: UUID
    prescription_number: Optional[str]
    citizen_id: UUID
    doctor_id: UUID
    appointment_id: Optional[UUID]
    health_unit_id: UUID
    items: List[PrescriptionItemSchema]
    status: str
    issue_date: date
    expiry_date: Optional[date]
    is_active: bool
    is_expired: bool
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class PrescriptionListSchema(BaseModel):
    """Prescription list response"""
    items: List[PrescriptionResponseSchema]
    total: int
    skip: int
    limit: int


class PrescriptionDispenseSchema(BaseModel):
    """Dispense prescription"""
    items_dispensed: Optional[List[str]] = None


class PrescriptionCancelSchema(BaseModel):
    """Cancel prescription"""
    reason: str = Field(..., min_length=5)
