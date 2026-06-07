from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from apps.backend.app.modules.resources.agricultura.api.deps import get_estoque_service
from apps.backend.app.modules.resources.agricultura.api.schemas.estoque_schema import (
    EstoqueCreate,
    EstoqueResponse,
)
from apps.backend.app.modules.resources.agricultura.application.services.estoque_service import (
    EstoqueService,
)
from apps.backend.app.modules.resources.agricultura.exceptions import (
    EstoqueNotFoundError,
    InsumoNotFoundError,
)

router = APIRouter(prefix="/estoques", tags=["Agricultura - estoques"])
estoque_service_dep = Depends(get_estoque_service)


@router.post("/", response_model=EstoqueResponse, status_code=status.HTTP_201_CREATED)
async def criar_controle_estoque(
    data: EstoqueCreate, service: EstoqueService = estoque_service_dep
):
    try:
        return await service.criar_controle(
            codigo_insumo=data.codigo_insumo, quantidade_minima=data.quantidade_minima
        )
    except InsumoNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get("/{codigo_estoque:path}", response_model=EstoqueResponse)
async def obter_estoque(
    codigo_estoque: str, service: EstoqueService = estoque_service_dep
):
    try:
        return await service.obter(codigo_estoque)
    except (EstoqueNotFoundError, InsumoNotFoundError) as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.get("/", response_model=list[EstoqueResponse])
async def listar_estoques(
    somente_baixo: bool = False, service: EstoqueService = estoque_service_dep
):
    return await service.listar(somente_baixo=somente_baixo)
