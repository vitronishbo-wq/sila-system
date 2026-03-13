from pydantic import BaseModel, Field, ConfigDict, EmailStr, field_validator
from typing import Optional, List, Dict, Any
from uuid import UUID
from datetime import datetime

class TaxpayerBase(BaseModel):
    """Base model para contribuinte"""
    nif: str = Field(..., description='NIF do contribuinte', min_length=9, max_length=14)
    name: str = Field(..., description='Nome completo', min_length=3, max_length=255)
    email: Optional[EmailStr] = Field(None, description='Email')
    phone: Optional[str] = Field(None, description='Telefone', min_length=9, max_length=20)
    address: Optional[str] = Field(None, description='Endereço', max_length=500)
    tax_regime: str = Field(..., description='Regime fiscal')

    @field_validator('nif')
    @classmethod
    def validate_nif(cls, v):
        if not v.isdigit() or len(v) not in [9, 14]:
            raise ValueError('NIF deve ter 9 ou 14 dígitos')
        return v

class TaxpayerCreate(TaxpayerBase):
    """Schema para criação de contribuinte"""
    pass

class TaxpayerUpdate(BaseModel):
    """Schema para atualização de contribuinte"""
    name: Optional[str] = Field(None, min_length=3, max_length=255)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, min_length=9, max_length=20)
    address: Optional[str] = Field(None, max_length=500)
    tax_regime: Optional[str] = None

class TaxpayerResponse(TaxpayerBase):
    """Schema para resposta de contribuinte"""
    id: UUID
    status: str
    registered_by: Optional[UUID]
    registered_at: datetime
    updated_at: Optional[datetime]
    agt_status: Optional[str]
    agt_last_sync: Optional[datetime]
    model_config = ConfigDict(from_attributes=True)

class TaxpayerListResponse(BaseModel):
    """Schema para listagem de contribuintes"""
    total: int
    items: List[TaxpayerResponse]
    page: int
    pages: int

class TaxpayerSummaryResponse(BaseModel):
    """Schema para resumo do contribuinte"""
    taxpayer: TaxpayerResponse
    statistics: Dict[str, Any]
    recent_declarations: List[Dict[str, Any]]
    pending_debts: List[Dict[str, Any]]
    recent_payments: List[Dict[str, Any]]