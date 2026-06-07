from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from apps.backend.app.modules.resources.pescas.api.deps import get_armador_service
from apps.backend.app.modules.resources.pescas.api.schemas.armador_schema import (
    ArmadorCreate,
    ArmadorFilter,
    ArmadorResponse,
)
from apps.backend.app.modules.resources.pescas.application.services.armador_service import (
    ArmadorService,
)

router = APIRouter(prefix="/armadores", tags=["Pescas - Armadores"])

armador_service_dep = Depends(get_armador_service)
filtros_dep = Depends()


@router.post("/", response_model=ArmadorResponse, status_code=status.HTTP_201_CREATED)
async def cadastrar_armador(
    data: ArmadorCreate, service: ArmadorService = armador_service_dep
):
    try:
        return await service.cadastrar_armador(nome=data.nome, nif=data.nif)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get("/{armador_id}", response_model=ArmadorResponse)
async def obter_armador(armador_id: UUID, service: ArmadorService = armador_service_dep):
    try:
        return await service.obter_armador(armador_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.get("/", response_model=list[ArmadorResponse])
async def listar_armadores(
    filtros: ArmadorFilter = filtros_dep, service: ArmadorService = armador_service_dep
):
    return await service.listar_armadores(ativo=filtros.ativo)