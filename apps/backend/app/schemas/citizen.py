from datetime import date, datetime
from uuid import UUID

from apps.backend.app.domain.enums import CitizenStatus, Gender, MaritalStatus
from pydantic import BaseModel, ConfigDict, EmailStr


class CitizenBase(BaseModel):
    national_id_number: str
    nif: str
    passport_number: str | None = None
    social_security_number: str | None = None
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
    alternative_phone: str | None = None
    email: EmailStr
    province: str
    municipality: str
    commune: str
    neighborhood: str
    street: str
    house_number: str
    geo_coordinates: str | None = None
    status: CitizenStatus = CitizenStatus.ACTIVE
    is_verified: bool = False
    verification_level: str = "basic"


class CitizenCreate(CitizenBase):
    created_by: str
    updated_by: str


class CitizenUpdate(BaseModel):
    national_id_number: str | None = None
    nif: str | None = None
    passport_number: str | None = None
    social_security_number: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    full_name: str | None = None
    gender: Gender | None = None
    birth_date: date | None = None
    marital_status: MaritalStatus | None = None
    nationality: str | None = None
    place_of_birth: str | None = None
    father_name: str | None = None
    mother_name: str | None = None
    phone: str | None = None
    alternative_phone: str | None = None
    email: EmailStr | None = None
    province: str | None = None
    municipality: str | None = None
    commune: str | None = None
    neighborhood: str | None = None
    street: str | None = None
    house_number: str | None = None
    geo_coordinates: str | None = None
    status: CitizenStatus | None = None
    is_verified: bool | None = None
    verification_level: str | None = None
    updated_by: str | None = None


class CitizenInDB(CitizenBase):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    created_at: datetime
    updated_at: datetime
    created_by: str
    updated_by: str


class CitizenOut(CitizenInDB):
    pass
