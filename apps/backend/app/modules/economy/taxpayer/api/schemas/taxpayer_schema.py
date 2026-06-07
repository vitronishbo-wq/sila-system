from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class TaxpayerBase(BaseModel):
    """Base model para contribuinte"""

    nif: str = Field(..., description="NIF do contribuinte", min_length=9, max_length=14)
    name: str = Field(..., description="Nome completo", min_length=3, max_length=255)
    email: EmailStr | None = Field(None, description="Email")
    phone: str | None = Field(None, description="Telefone", min_length=9, max_length=20)
    address: str | None = Field(None, description="Endereço", max_length=500)
    tax_regime: str = Field(..., description="Regime fiscal")

    @field_validator("nif")
    @classmethod
    def validate_nif(cls, v):
        if not v.isdigit() or len(v) not in [9, 14]:
            raise ValueError("NIF deve ter 9 ou 14 dígitos")
        return v


class TaxpayerCreate(TaxpayerBase):
    """Schema para criação de contribuinte"""

    pass


class TaxpayerUpdate(BaseModel):
    """Schema para atualização de contribuinte"""

    name: str | None = Field(None, min_length=3, max_length=255)
    email: EmailStr | None = None
    phone: str | None = Field(None, min_length=9, max_length=20)
    address: str | None = Field(None, max_length=500)
    tax_regime: str | None = None


class TaxpayerResponse(TaxpayerBase):
    """Schema para resposta de contribuinte"""

    id: UUID
    status: str
    registered_by: UUID | None
    registered_at: datetime
    updated_at: datetime | None
    agt_status: str | None
    agt_last_sync: datetime | None
    model_config = ConfigDict(from_attributes=True)


class TaxpayerListResponse(BaseModel):
    """Schema para listagem de contribuintes"""

    total: int
    items: list[TaxpayerResponse]
    page: int
    pages: int


class TaxpayerSummaryResponse(BaseModel):
    """Schema para resumo do contribuinte"""

    taxpayer: TaxpayerResponse
    statistics: dict[str, Any]
    recent_declarations: list[dict[str, Any]]
    pending_debts: list[dict[str, Any]]
    recent_payments: list[dict[str, Any]]
