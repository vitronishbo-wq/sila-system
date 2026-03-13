from __future__ import annotations
from datetime import date
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.domain.enums import StatusOutorga, TipoOperadora, TipoServico

class OperadoraCreate(BaseModel):
    cnpj: str = Field(..., pattern='^\\d{2}\\.\\d{3}\\.\\d{3}/\\d{4}-\\d{2}$')
    razao_social: str = Field(..., min_length=3)
    tipo: TipoOperadora
    servicos_autorizados: list[TipoServico] = Field(..., min_length=1)
    endereco: str
    municipio: str
    provincia: str
    telefone: str
    email: str
    representante_legal: str
    representante_documento: str
    representante_cargo: str
    nome_fantasia: str | None = None
    observacoes: str | None = None

class OperadoraAuthorize(BaseModel):
    outorga_id: UUID
    data_autorizacao: date
    data_validade: date

class OperadoraResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    cnpj: str
    razao_social: str
    nome_fantasia: str | None = None
    tipo: TipoOperadora
    servicos_autorizados: list[TipoServico]
    municipio: str
    provincia: str
    status: StatusOutorga
    data_autorizacao: date | None = None
    data_validade: date | None = None
    ativo: bool