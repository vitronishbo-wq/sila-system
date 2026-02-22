from datetime import datetime, date
from typing import Optional, List
from pydantic import BaseModel, EmailStr
from modules.identity.models.user import AdministrativeLevel


class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None
    birth_date: Optional[date] = None
    gender: Optional[str] = None
    administrative_level: AdministrativeLevel = AdministrativeLevel.LOCAL
    region_id: Optional[int] = None
    is_active: bool = True


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None
    birth_date: Optional[date] = None
    gender: Optional[str] = None
    password: Optional[str] = None
    administrative_level: Optional[AdministrativeLevel] = None
    region_id: Optional[int] = None
    is_active: Optional[bool] = None


class UserResponse(BaseModel):
    id: int
    uuid: str
    email: EmailStr
    full_name: Optional[str] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None
    birth_date: Optional[date] = None
    gender: Optional[str] = None
    administrative_level: AdministrativeLevel
    region_id: Optional[int] = None
    is_active: bool
    roles: List[str]
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime] = None

    class Config:
        from_attributes = True
