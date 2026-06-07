from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator


class DeclarationBase(BaseModel):
    """Base model para declaração"""

    tax_type: str = Field(..., description="Tipo de imposto (IVA, IRS, IRC)")
    tax_period: str = Field(..., description="Período fiscal (YYYY-MM)")
    gross_amount: float = Field(..., gt=0, description="Valor bruto")
    deductions: float | None = Field(0, ge=0, description="Deduções")

    @field_validator("tax_period")
    @classmethod
    def validate_period(cls, v):
        try:
            year, month = v.split("-")
            if not 1 <= int(month) <= 12:
                raise ValueError()
        except:
            raise ValueError("Período deve estar no formato YYYY-MM") from None
        return v


class DeclarationCreate(DeclarationBase):
    """Schema para criação de declaração"""

    pass


class DeclarationResponse(DeclarationBase):
    """Schema para resposta de declaração"""

    id: UUID
    taxpayer_id: UUID
    declaration_number: str
    net_amount: float
    declaration_date: date
    due_date: date
    status: str
    protocol: str | None
    submitted_by: UUID
    submitted_at: datetime
    processed_by: UUID | None
    processed_at: datetime | None
    observations: str | None
    model_config = ConfigDict(from_attributes=True)


class DeclarationListResponse(BaseModel):
    """Schema para listagem de declarações"""

    total: int
    items: list[DeclarationResponse]


class DeclarationStatusUpdate(BaseModel):
    """Schema para atualização de status"""

    status: str = Field(..., description="Novo status")
    observations: str | None = None
