from __future__ import annotations
from datetime import date
from uuid import UUID
from pydantic import BaseModel, ConfigDict
from apps.backend.app.modules.resources.agricultura.domain.enums import StatusCertificacao

class CertificacaoCreate(BaseModel):
    codigo_propriedade: str
    tipo: str
    orgao_emissor: str

class CertificacaoAprovacaoInput(BaseModel):
    data_validade: date | None = None

class CertificacaoReprovacaoInput(BaseModel):
    motivo: str

class CertificacaoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    codigo_certificacao: str
    codigo_propriedade: str
    tipo: str
    orgao_emissor: str
    status: StatusCertificacao
    data_solicitacao: date
    data_emissao: date | None = None
    data_validade: date | None = None
    motivo_reprovacao: str | None = None