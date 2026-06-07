from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr

from ...domain.enums import CitizenStatusEnum, GenderEnum, MaritalStatusEnum


class CitizenCreateSchema(BaseModel):
    national_id_number: str
    nif: str
    passport_number: str | None = None
    social_security_number: str | None = None
    first_name: str
    last_name: str
    full_name: str
    gender: GenderEnum
    birth_date: date
    marital_status: MaritalStatusEnum
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
    verification_level: str | None = "BASIC"
    created_by: str
    updated_by: str


class CitizenUpdateSchema(BaseModel):
    national_id_number: str | None = None
    nif: str | None = None
    passport_number: str | None = None
    social_security_number: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    full_name: str | None = None
    gender: GenderEnum | None = None
    birth_date: date | None = None
    marital_status: MaritalStatusEnum | None = None
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
    verification_level: str | None = None
    updated_by: str | None = None


class CitizenReadSchema(BaseModel):
    id: UUID
    national_id_number: str
    nif: str
    passport_number: str | None
    social_security_number: str | None
    first_name: str
    last_name: str
    full_name: str
    gender: GenderEnum
    birth_date: date
    marital_status: MaritalStatusEnum
    nationality: str
    place_of_birth: str
    father_name: str
    mother_name: str
    phone: str
    alternative_phone: str | None
    email: EmailStr
    province: str
    municipality: str
    commune: str
    neighborhood: str
    street: str
    house_number: str
    geo_coordinates: str | None
    status: CitizenStatusEnum
    is_verified: bool
    verification_level: str
    created_at: datetime
    updated_at: datetime
    created_by: str
    updated_by: str

    class Config:
        from_attributes = True
