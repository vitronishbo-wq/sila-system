from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class CertificateBase(BaseModel):
    """Base model para certidão"""

    certificate_type: str = Field(..., description="Tipo de certidão")
    year: int | None = Field(None, description="Ano de referência")
    purpose: str | None = Field(None, max_length=500, description="Finalidade")


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
    issued_at: datetime | None
    issued_by: UUID | None
    expires_at: date | None
    file_url: str | None
    error_message: str | None
    model_config = ConfigDict(from_attributes=True)


class CertificateListResponse(BaseModel):
    """Schema para listagem de certidões"""

    total: int
    items: list[CertificateResponse]


class CertificateDownloadResponse(BaseModel):
    """Schema para download de certidão"""

    content: bytes
    filename: str
    content_type: str = "application/pdf"
