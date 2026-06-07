from __future__ import annotations

from datetime import date
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from apps.backend.app.modules.society.juventude.domain.enums import StatusAcompanhamento


class AcompanhamentoJuvenilCreate(BaseModel):
    jovem_id: UUID
    responsavel: str = Field(..., min_length=3)
    objetivo: str = Field(..., min_length=3)
    data_inicio: date
    proxima_revisao: date | None = None
    observacoes: str | None = None


class AcompanhamentoJuvenilEvolucao(BaseModel):
    descricao: str = Field(..., min_length=3)
    proxima_revisao: date | None = None


class AcompanhamentoJuvenilEncerrar(BaseModel):
    observacoes: str | None = None


class AcompanhamentoJuvenilResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    codigo_acompanhamento: str
    jovem_id: UUID
    responsavel: str
    objetivo: str
    data_inicio: date
    data_registo: date
    status: StatusAcompanhamento
    proxima_revisao: date | None = None
    historico: list[dict] | None = None
    observacoes: str | None = None
    ativo: bool
