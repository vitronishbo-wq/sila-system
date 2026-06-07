from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from apps.backend.app.modules.economy.taxpayer.domain.enums.taxpayer_status import TaxpayerStatus


class TaxpayerBase(BaseModel):
    tenant_id: UUID | None
    citizen_id: UUID | None
    nif: str = Field(..., min_length=1)
    name: str = Field(..., min_length=1)


class TaxpayerCreate(TaxpayerBase):
    pass


class TaxpayerUpdate(BaseModel):
    name: str | None
    nif: str | None


class TaxpayerRead(TaxpayerBase):
    id: UUID
    status: TaxpayerStatus
    created_at: datetime
    updated_at: datetime | None
    version: int

    class Config:
        from_attributes = True
