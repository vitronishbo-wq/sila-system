"""Health Unit Schemas"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from uuid import UUID


class HealthUnitCreateSchema(BaseModel):
    """Create health unit"""
    code: str = Field(..., min_length=2)
    name: str = Field(..., min_length=5)
    unit_type: str
    province: str
    municipality: str
    address: str
    commune: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    beds: int = 0
    has_emergency: bool = False
    has_laboratory: bool = False
    has_pharmacy: bool = False


class HealthUnitResponseSchema(BaseModel):
    """Health unit response"""
    id: UUID
    code: str
    name: str
    unit_type: str
    province: str
    municipality: str
    address: str
    commune: Optional[str]
    phone: Optional[str]
    email: Optional[str]
    beds: int
    has_emergency: bool
    has_laboratory: bool
    has_pharmacy: bool
    specialties: List[str]
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class HealthUnitListSchema(BaseModel):
    """Health unit list response"""
    items: List[HealthUnitResponseSchema]
    total: int
    skip: int
    limit: int


class HealthUnitSpecialtySchema(BaseModel):
    """Add specialty"""
    specialty: str = Field(..., min_length=3)


class HealthProfessionalRegisterSchema(BaseModel):
    """Register health professional"""
    user_id: UUID
    health_unit_id: UUID
    license_number: str
    specialization: str


class HealthProfessionalResponseSchema(BaseModel):
    """Health professional response"""
    id: UUID
    user_id: UUID
    health_unit_id: UUID
    license_number: str
    specialization: str
    created_at: datetime
    
    class Config:
        from_attributes = True
