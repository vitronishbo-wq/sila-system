from __future__ import annotations

from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict

from apps.backend.app.modules.resources.pescas.api.deps import get_rastreabilidade_service
from apps.backend.app.modules.resources.pescas.application.services.rastreabilidade_service import (
    RastreabilidadeService,
)

router = APIRouter(prefix="/rastreabilidade", tags=["Pescas - Rastreabilidade"])

rastreabilidade_service_dep = Depends(get_rastreabilidade_service)


class RastreabilidadeCreate(BaseModel):
    lote_codigo: str
    origem_captura_id: UUID
    etapa: str
    operador: str


class RastreabilidadeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    lote_codigo: str
    origem_captura_id: UUID
    etapa: str
    data_evento: datetime
    operador: str
    observacoes: str | None = None


@router.post("/", response_model=RastreabilidadeResponse, status_code=status.HTTP_201_CREATED)
async def registrar_evento(
    data: RastreabilidadeCreate,
    service: RastreabilidadeService = rastreabilidade_service_dep,
):
    return await service.registrar_evento(
        lote_codigo=data.lote_codigo,
        origem_captura_id=data.origem_captura_id,
        etapa=data.etapa,
        operador=data.operador,
    )


@router.get("/", response_model=list[RastreabilidadeResponse])
async def listar_eventos(service: RastreabilidadeService = rastreabilidade_service_dep):
    return await service.listar()