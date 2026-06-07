from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from apps.backend.app.modules.resources.agricultura.domain.enums import TipoOperacao


class OperacaoCreate(BaseModel):
    codigo_safra: str
    tipo: TipoOperacao
    descricao: str
    codigo_insumo: str | None = None
    quantidade_insumo: float | None = None


class OperacaoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    codigo_operacao: str
    codigo_safra: str
    tipo: TipoOperacao
    descricao: str
    data_operacao: datetime
    codigo_insumo: str | None = None
    quantidade_insumo: float | None = None
