from __future__ import annotations

from datetime import date
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from apps.backend.app.modules.resources.aguas_saneamento.domain.enums import (
    StatusOutorga,
    TipoCaptacao,
    TipoOutorga,
    TipoUso,
)


class OutorgaCreate(BaseModel):
    tipo: TipoOutorga
    requerente_id: UUID
    requerente_tipo: str
    corpo_hidrico_id: UUID
    tipo_captacao: TipoCaptacao | None = None
    vazao: Decimal
    unidade_vazao: str
    tempo_captacao: int | None = None
    periodo_captacao: str | None = None
    finalidade_uso: TipoUso
    coordenadas_lat: Decimal | None = None
    coordenadas_long: Decimal | None = None


class OutorgaDeferimentoInput(BaseModel):
    data_validade_inicio: date
    data_validade_fim: date
    data_publicacao: date
    processo: str


class OutorgaMotivoInput(BaseModel):
    motivo: str


class OutorgaRenovacaoInput(BaseModel):
    nova_data_fim: date


class OutorgaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    numero_outorga: str
    tipo: TipoOutorga
    status: StatusOutorga
    requerente_id: UUID
    requerente_tipo: str
    corpo_hidrico_id: UUID
    tipo_captacao: TipoCaptacao | None = None
    vazao: Decimal
    unidade_vazao: str
    tempo_captacao: int | None = None
    periodo_captacao: str | None = None
    finalidade_uso: TipoUso
    data_requerimento: date
    data_validade_inicio: date | None = None
    data_validade_fim: date | None = None
    data_publicacao: date | None = None
    processo_administrativo: str | None = None
    coordenadas_lat: Decimal | None = None
    coordenadas_long: Decimal | None = None
    observacoes: str | None = None
