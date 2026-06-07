from __future__ import annotations

from datetime import date
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from apps.backend.app.modules.educacao.domain.enums import StatusFluxo, TipoInscricao


class InscricaoCreate(BaseModel):
    citizen_id: UUID = Field(..., description="ID do cidadao no nucleo identity")
    escola_id: UUID
    observacoes: str | None = None


class InscricaoConfirmar(BaseModel):
    confirmacao_documental: Literal[True]


class InscricaoCancelar(BaseModel):
    motivo: str = Field(..., min_length=3, max_length=500)


class InscricaoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    numero_processo: str
    tipo: TipoInscricao
    citizen_id: UUID
    escola_id: UUID
    data_inscricao: date
    status: StatusFluxo
    observacoes: str | None = None
