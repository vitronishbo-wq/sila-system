from __future__ import annotations
from typing import Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field
from apps.backend.app.modules.economy.taxpayer.domain.enums.taxpayer_status import TaxpayerStatus

class TaxpayerBase(BaseModel):
    tenant_id: Optional[UUID]
    citizen_id: Optional[UUID]
    nif: str = Field(..., min_length=1)
    name: str = Field(..., min_length=1)

class TaxpayerCreate(TaxpayerBase):
    pass

class TaxpayerUpdate(BaseModel):
    name: Optional[str]
    nif: Optional[str]

class TaxpayerRead(TaxpayerBase):
    id: UUID
    status: TaxpayerStatus
    created_at: datetime
    updated_at: Optional[datetime]
    version: int

    class Config:
        from_attributes = True