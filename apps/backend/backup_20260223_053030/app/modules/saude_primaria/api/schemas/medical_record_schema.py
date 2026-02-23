"""Medical Record Schemas"""
from pydantic import BaseModel, Field
from datetime import datetime, date
from typing import Optional, List
from uuid import UUID


class VitalSignsSchema(BaseModel):
    """Vital signs"""
    blood_pressure_systolic: Optional[int] = None
    blood_pressure_diastolic: Optional[int] = None
    heart_rate: Optional[int] = None
    respiratory_rate: Optional[int] = None
    temperature: Optional[float] = None
    oxygen_saturation: Optional[int] = None
    weight: Optional[float] = None
    height: Optional[float] = None


class MedicalRecordCreateSchema(BaseModel):
    """Create medical record"""
    citizen_id: UUID
    doctor_id: UUID
    health_unit_id: UUID
    chief_complaint: str = Field(..., min_length=5)
    appointment_id: Optional[UUID] = None
    history_of_present_illness: Optional[str] = None
    past_medical_history: Optional[str] = None
    family_history: Optional[str] = None
    social_history: Optional[str] = None
    allergies: Optional[List[str]] = None
    physical_exam: Optional[str] = None
    treatment_plan: Optional[str] = None
    recommendations: Optional[str] = None


class MedicalRecordResponseSchema(BaseModel):
    """Medical record response"""
    id: UUID
    record_number: Optional[str]
    citizen_id: UUID
    doctor_id: UUID
    health_unit_id: UUID
    chief_complaint: str
    diagnosis: List[str]
    diagnosis_codes: List[str]
    allergies: List[str]
    treatment_plan: Optional[str]
    recommendations: Optional[str]
    follow_up_date: Optional[date]
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class MedicalRecordListSchema(BaseModel):
    """Medical record list response"""
    items: List[MedicalRecordResponseSchema]
    total: int
    skip: int
    limit: int


class DiagnosisAddSchema(BaseModel):
    """Add diagnosis"""
    diagnosis: str
    code: Optional[str] = None


class VitalSignsUpdateSchema(BaseModel):
    """Update vital signs"""
    vital_signs: VitalSignsSchema
