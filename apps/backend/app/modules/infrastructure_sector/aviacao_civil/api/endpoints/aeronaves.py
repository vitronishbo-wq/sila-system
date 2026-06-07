from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from apps.backend.app.modules.infrastructure_sector.aviacao_civil.api.deps import (
    get_aeronave_service,
)
from apps.backend.app.modules.infrastructure_sector.aviacao_civil.api.schemas.aeronave_schema import (
    AeronaveCreate,
    AeronaveResponse,
)
from apps.backend.app.modules.infrastructure_sector.aviacao_civil.application.services.aeronave_service import (
    AeronaveService,
)

router = APIRouter(prefix="/aeronaves", tags=["Aviacao Civil - Aeronaves"])
aeronave_service_dep = Depends(get_aeronave_service)


@router.post("/", response_model=AeronaveResponse, status_code=status.HTTP_201_CREATED)
async def criar_aeronave(
    payload: AeronaveCreate, service: AeronaveService = aeronave_service_dep
) -> AeronaveResponse:
    try:
        aeronave = await service.registrar_aeronave(**payload.model_dump())
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    return AeronaveResponse.model_validate(aeronave)


@router.get("/", response_model=list[AeronaveResponse])
async def listar_aeronaves(
    service: AeronaveService = aeronave_service_dep,
) -> list[AeronaveResponse]:
    aeronaves = await service.listar_aeronaves()
    return [AeronaveResponse.model_validate(item) for item in aeronaves]


@router.get("/{aeronave_id}", response_model=AeronaveResponse)
async def obter_aeronave(
    aeronave_id: UUID, service: AeronaveService = aeronave_service_dep
) -> AeronaveResponse:
    try:
        aeronave = await service.buscar_aeronave(aeronave_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    return AeronaveResponse.model_validate(aeronave)
