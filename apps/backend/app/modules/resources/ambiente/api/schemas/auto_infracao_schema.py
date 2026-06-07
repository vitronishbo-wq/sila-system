from __future__ import annotations

from datetime import date
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from apps.backend.app.modules.resources.ambiente.domain.enums import (
    StatusAutoInfracao,
    TipoAutoInfracao,
)


class AutoInfracaoCreate(BaseModel):
    numero_fiscalizacao: str
    tipo: TipoAutoInfracao
    descricao: str
    fiscal_id: UUID
    valor_multa: Decimal | None = None


class AutoInfracaoJulgamentoInput(BaseModel):
    mantido: bool
    observacoes: str | None = None


class AutoInfracaoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    numero_auto: str
    numero_fiscalizacao: str
    tipo: TipoAutoInfracao
    descricao: str
    fiscal_id: UUID
    status: StatusAutoInfracao
    data_lavratura: date
    valor_multa: Decimal | None = None
    observacoes: str | None = None
