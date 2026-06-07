from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from apps.backend.app.modules.resources.florestas.api.deps import get_manejo_service
from apps.backend.app.modules.resources.florestas.api.schemas.unidade_manejo_schema import (
    UnidadeManejoCreate,
    UnidadeManejoResponse,
)
from apps.backend.app.modules.resources.florestas.application.services.manejo_service import (
    ManejoService,
)

router = APIRouter(prefix="/unidades-manejo", tags=["Florestas - Unidades Manejo"])

manejo_service_dep = Depends(get_manejo_service)


@router.post("/", response_model=UnidadeManejoResponse, status_code=201)
async def cadastrar_unidade(
    data: UnidadeManejoCreate, service: ManejoService = manejo_service_dep
):
    try:
        return await service.cadastrar_unidade(
            nome=data.nome,
            area_total_ha=data.area_total_ha,
            tipo_manejo=data.tipo_manejo,
            ciclo_corte=data.ciclo_corte,
            operador_id=data.operador_id,
            imovel_id=data.imovel_id,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/{unidade_id}", response_model=UnidadeManejoResponse)
async def obter_unidade(unidade_id: UUID, service: ManejoService = manejo_service_dep):
    try:
        return await service.buscar_unidade(unidade_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/", response_model=list[UnidadeManejoResponse])
async def listar_unidades(operador_id: UUID, service: ManejoService = manejo_service_dep):
    return await service.listar_unidades(operador_id)