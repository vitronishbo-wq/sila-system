from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from uuid import UUID
from datetime import date, datetime


class CertificateBase(BaseModel):
    """Base model para certidão"""
    certificate_type: str = Field(..., description="Tipo de certidão")
    year: Optional[int] = Field(None, description="Ano de referência")
    purpose: Optional[str] = Field(None, max_length=500, description="Finalidade")


class CertificateCreate(CertificateBase):
    """Schema para solicitação de certidão"""
    pass


class CertificateResponse(CertificateBase):
    """Schema para resposta de certidão"""
    id: UUID
    taxpayer_id: UUID
    certificate_number: str
    status: str
    requested_at: datetime
    requested_by: UUID
    issued_at: Optional[datetime]
    issued_by: Optional[UUID]
    expires_at: Optional[date]
    file_url: Optional[str]
    error_message: Optional[str]
    
    model_config = ConfigDict(from_attributes=True)


class CertificateListResponse(BaseModel):
    """Schema para listagem de certidões"""
    total: int
    items: List[CertificateResponse]


class CertificateDownloadResponse(BaseModel):
    """Schema para download de certidão"""
    content: bytes
    filename: str
    content_type: str = "application/pdf"
