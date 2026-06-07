from __future__ import annotations

from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status

from apps.backend.app.modules.infrastructure_sector.aviacao_civil.api.deps import get_voo_service
from apps.backend.app.modules.infrastructure_sector.aviacao_civil.api.schemas.voo_schema import (
    VooCreate,
    VooResponse,
    VooStatusInput,
)
from apps.backend.app.modules.infrastructure_sector.aviacao_civil.application.services.voo_service import (
    VooService,
)

router = APIRouter(prefix="/voos", tags=["Aviacao Civil - Voos"])
voo_service_dep = Depends(get_voo_service)
data_query = Query(..., description="Data base para o consolidado diario")


@router.post("/", response_model=VooResponse, status_code=status.HTTP_201_CREATED)
async def programar_voo(
    payload: VooCreate, service: VooService = voo_service_dep
) -> VooResponse:
    try:
        voo = await service.programar_voo(**payload.model_dump())
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    return VooResponse.model_validate(voo)


@router.post("/{voo_id}/decolagem", response_model=VooResponse)
async def registrar_decolagem(
    voo_id: UUID, payload: VooStatusInput, service: VooService = voo_service_dep
) -> VooResponse:
    try:
        voo = await service.registrar_decolagem(voo_id=voo_id, data_hora=payload.data_hora)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    return VooResponse.model_validate(voo)


@router.post("/{voo_id}/pouso", response_model=VooResponse)
async def registrar_pouso(
    voo_id: UUID, payload: VooStatusInput, service: VooService = voo_service_dep
) -> VooResponse:
    try:
        voo = await service.registrar_pouso(voo_id=voo_id, data_hora=payload.data_hora)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    return VooResponse.model_validate(voo)


@router.get("/ativos", response_model=list[VooResponse])
async def listar_voos_ativos(service: VooService = voo_service_dep) -> list[VooResponse]:
    voos = await service.get_voos_ativos()
    return [VooResponse.model_validate(item) for item in voos]


@router.get("/estatisticas/dia")
async def estatisticas_dia(
    data: datetime = data_query,
    service: VooService = voo_service_dep,
) -> dict:
    return await service.get_estatisticas_dia(data=data)
