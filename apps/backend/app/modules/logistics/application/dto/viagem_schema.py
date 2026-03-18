from __future__ import annotations
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict
from apps.backend.app.modules.logistics.domain.enums import StatusViagem

class ViagemCreate(BaseModel):
    linha_id: UUID
    veiculo_id: UUID
    motorista_id: UUID
    data_hora_saida: datetime
    data_hora_chegada_prevista: datetime
    origem: str
    destino: str
    itinerario: list[dict] | None = None
    observacoes: str | None = None

class ViagemConcluirInput(BaseModel):
    data_hora_chegada: datetime

class ViagemCancelarInput(BaseModel):
    motivo: str

class ViagemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    linha_id: UUID
    veiculo_id: UUID
    motorista_id: UUID
    data_hora_saida: datetime
    data_hora_chegada_prevista: datetime
    data_hora_chegada_real: datetime | None = None
    origem: str
    destino: str
    itinerario: list[dict]
    status: StatusViagem
    observacoes: str | None = None