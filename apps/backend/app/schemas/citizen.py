from typing import Optional
from uuid import UUID
from datetime import date, datetime
from pydantic import BaseModel, EmailStr, ConfigDict

from app.domain.enums import Gender, MaritalStatus, CitizenStatus

class CitizenBase(BaseModel):
    national_id_number: str
    nif: str
    passport_number: Optional[str] = None
    social_security_number: Optional[str] = None
    first_name: str
    last_name: str
    full_name: str
    gender: Gender
    birth_date: date
    marital_status: MaritalStatus
    nationality: str
    place_of_birth: str
    father_name: str
    mother_name: str
    phone: str
    alternative_phone: Optional[str] = None
    email: EmailStr
    province: str
    municipality: str
    commune: str
    neighborhood: str
    street: str
    house_number: str
    geo_coordinates: Optional[str] = None
    status: CitizenStatus = CitizenStatus.ACTIVE
    is_verified: bool = False
    verification_level: str = "basic"

class CitizenCreate(CitizenBase):
    created_by: str
    updated_by: str

class CitizenUpdate(BaseModel):
    national_id_number: Optional[str] = None
    nif: Optional[str] = None
    passport_number: Optional[str] = None
    social_security_number: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    full_name: Optional[str] = None
    gender: Optional[Gender] = None
    birth_date: Optional[date] = None
    marital_status: Optional[MaritalStatus] = None
    nationality: Optional[str] = None
    place_of_birth: Optional[str] = None
    father_name: Optional[str] = None
    mother_name: Optional[str] = None
    phone: Optional[str] = None
    alternative_phone: Optional[str] = None
    email: Optional[EmailStr] = None
    province: Optional[str] = None
    municipality: Optional[str] = None
    commune: Optional[str] = None
    neighborhood: Optional[str] = None
    street: Optional[str] = None
    house_number: Optional[str] = None
    geo_coordinates: Optional[str] = None
    status: Optional[CitizenStatus] = None
    is_verified: Optional[bool] = None
    verification_level: Optional[str] = None
    updated_by: Optional[str] = None

class CitizenInDB(CitizenBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    created_at: datetime
    updated_at: datetime
    created_by: str
    updated_by: str

class CitizenOut(CitizenInDB):
    pass
