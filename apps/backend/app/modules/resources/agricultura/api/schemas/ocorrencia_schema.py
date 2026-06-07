from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from apps.backend.app.modules.resources.agricultura.domain.enums import (
    SeveridadeOcorrencia,
    StatusOcorrencia,
)


class OcorrenciaCreate(BaseModel):
    codigo_propriedade: str
    praga_doenca: str
    descricao: str
    severidade: SeveridadeOcorrencia
    cultura_afetada: str | None = None
    acao_recomendada: str | None = None


class OcorrenciaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    codigo_ocorrencia: str
    codigo_propriedade: str
    praga_doenca: str
    descricao: str
    severidade: SeveridadeOcorrencia
    status: StatusOcorrencia
    data_registro: datetime
    cultura_afetada: str | None = None
    acao_recomendada: str | None = None
    data_resolucao: datetime | None = None
