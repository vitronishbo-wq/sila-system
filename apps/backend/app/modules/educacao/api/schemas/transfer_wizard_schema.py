from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, Field


class TransferWizardResponse(BaseModel):
    id: uuid.UUID
    citizen_id: uuid.UUID
    status: str
    passo_atual: int
    origem_escola_id: Optional[uuid.UUID] = None
    origem_classe: Optional[str] = None
    destino_escola_id: Optional[uuid.UUID] = None
    destino_classe: Optional[str] = None
    destino_turno: Optional[str] = None
    motivo: Optional[str] = None
    elegibilidade: Optional[dict] = None
    reserva_id: Optional[uuid.UUID] = None
    transferencia_id: Optional[uuid.UUID] = None
    created_at: datetime
    expires_at: datetime


class Passo1OrigemRequest(BaseModel):
    origem_escola_id: uuid.UUID
    origem_classe: str = Field(..., min_length=1, max_length=32)


class Passo2DestinoRequest(BaseModel):
    destino_escola_id: uuid.UUID
    destino_classe: str = Field(..., min_length=1, max_length=32)
    destino_turno: str = Field(..., min_length=1, max_length=32)
    motivo: str = Field("", max_length=500)


class Passo4ReservarRequest(BaseModel):
    student_id: uuid.UUID
    ano_letivo: str = "2026"


class Passo5ConfirmarRequest(BaseModel):
    transferencia_id: uuid.UUID


class ElegibilidadeResponse(BaseModel):
    elegivel: bool
    score: int
    motivos: list[str]
    tem_vaga: bool
    mesma_rede: bool
    classes_compativeis: bool
    ano_letivo: str


class IniciarResponse(BaseModel):
    wizard_id: uuid.UUID
    status: str
    passo_atual: int
    expires_at: datetime
