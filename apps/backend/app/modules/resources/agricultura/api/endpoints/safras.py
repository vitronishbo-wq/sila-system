from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from apps.backend.app.modules.resources.agricultura.api.deps import get_safra_service
from apps.backend.app.modules.resources.agricultura.api.schemas.safra_schema import (
    ColheitaInput,
    SafraCreate,
    SafraResponse,
)
from apps.backend.app.modules.resources.agricultura.application.services.safra_service import (
    SafraService,
)
from apps.backend.app.modules.resources.agricultura.exceptions import (
    CulturaNotFoundError,
    PropriedadeNotFoundError,
    SafraNotFoundError,
)

router = APIRouter(prefix="/safras", tags=["Agricultura - safras"])
safra_service_dep = Depends(get_safra_service)


@router.post("/", response_model=SafraResponse, status_code=status.HTTP_201_CREATED)
async def criar_safra(data: SafraCreate, service: SafraService = safra_service_dep):
    try:
        return await service.criar_safra(
            codigo_propriedade=data.codigo_propriedade,
            codigo_cultura=data.codigo_cultura,
            ano=data.ano,
            area_plantada_ha=data.area_plantada_ha,
            producao_estimada_ton=data.producao_estimada_ton,
        )
    except (ValueError, PropriedadeNotFoundError, CulturaNotFoundError) as exc:
        code = (
            status.HTTP_404_NOT_FOUND
            if isinstance(exc, (PropriedadeNotFoundError, CulturaNotFoundError))
            else status.HTTP_400_BAD_REQUEST
        )
        raise HTTPException(status_code=code, detail=str(exc)) from exc


@router.post("/{codigo_safra:path}/iniciar", response_model=SafraResponse)
async def iniciar_safra(codigo_safra: str, service: SafraService = safra_service_dep):
    try:
        return await service.iniciar(codigo_safra)
    except SafraNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/{codigo_safra:path}/colher", response_model=SafraResponse)
async def colher_safra(
    codigo_safra: str, data: ColheitaInput, service: SafraService = safra_service_dep
):
    try:
        return await service.colher(codigo_safra, data.producao_real_ton)
    except SafraNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get("/{codigo_safra:path}", response_model=SafraResponse)
async def obter_safra(codigo_safra: str, service: SafraService = safra_service_dep):
    try:
        return await service.obter(codigo_safra)
    except SafraNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.get("/", response_model=list[SafraResponse])
async def listar_safras(service: SafraService = safra_service_dep):
    return await service.listar()
