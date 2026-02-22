from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, List

class PaymentBase(BaseModel):
    amount: float
    provider: str = "multicaixa"

class PaymentCreate(PaymentBase):
    request_id: Optional[int] = None

class PaymentRead(PaymentBase):
    id: int
    reference: str
    status: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class WorkflowRead(BaseModel):
    id: int
    name: str
    module_slug: str
    definition: dict
    status: str
    model_config = ConfigDict(from_attributes=True)

class ProcessRead(BaseModel):
    id: int
    service_id: int
    citizen_id: int
    status: str
    current_step: str
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


class ServiceRead(BaseModel):
    id: int
    code: str
    name: str
    scope: str
    is_active: bool
    model_config = ConfigDict(from_attributes=True)


class CitizenRead(BaseModel):
    id: int
    full_name: str
    bi_number: str
    province: str
    municipality: str
    model_config = ConfigDict(from_attributes=True)


class RequestRead(BaseModel):
    id: int
    service_id: int
    citizen_id: int
    status: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
