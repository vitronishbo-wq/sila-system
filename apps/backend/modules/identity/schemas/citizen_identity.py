from datetime import date, datetime
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from enum import Enum

class GenderEnum(str, Enum):
    MALE = "M"
    FEMALE = "F"
    OTHER = "O"

class CitizenIdentityBase(BaseModel):
    full_name: Optional[str] = Field(None, min_length=3, max_length=255)
    # Validação rigorosa para o Bilhete de Identidade Angolano
    bi_number: Optional[str] = Field(None, pattern=r'^\d{9}[A-Z]{2}\d{3}$') 
    email: EmailStr
    birth_date: Optional[date] = None
    gender: Optional[GenderEnum] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None

class CitizenIdentityCreate(CitizenIdentityBase):
    password: str = Field(..., min_length=8)

class CitizenIdentityUpdate(BaseModel):
    full_name: Optional[str] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None
    is_active: Optional[bool] = None

class CitizenIdentityRead(CitizenIdentityBase):
    id: int
    uuid: Optional[UUID] = None 
    is_active: bool
    is_superuser: bool = False
    roles: List[str] = []
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

# --- AS CLASSES QUE FALTAVAM E CAUSAVAM O ERRO ---

class CitizenIdentityWithRelations(CitizenIdentityRead):
    """
    Schema para retorno do perfil com relações.
    Essencial para o endpoint /me funcionar.
    """
    pass

class CitizenIdentitySummary(BaseModel):
    id: int
    full_name: str
    bi_number: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)

class IdentityStats(BaseModel):
    total_citizens: int
    active_now: int
    pending_verifications: int