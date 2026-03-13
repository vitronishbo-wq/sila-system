from __future__ import annotations
from datetime import date
from uuid import UUID
from pydantic import BaseModel, ConfigDict
from app.modules.resources.aguas_saneamento.domain.enums import StatusAbastecimento

class AbastecimentoCreate(BaseModel):
    infraestrutura_id: UUID
    nome_sistema: str
    provincia: str
    municipio: str

class AbastecimentoOperacaoInput(BaseModel):
    data_inicio_operacao: date | None = None

class AbastecimentoMotivoInput(BaseModel):
    motivo: str

class AbastecimentoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    codigo_abastecimento: str
    infraestrutura_id: UUID
    nome_sistema: str
    provincia: str
    municipio: str
    status: StatusAbastecimento
    data_registro: date
    data_inicio_operacao: date | None = None
    data_interrupcao: date | None = None
    motivo_interrupcao: str | None = None
    observacoes: str | None = None