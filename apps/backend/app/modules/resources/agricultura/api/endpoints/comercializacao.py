from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from apps.backend.app.modules.resources.agricultura.api.deps import get_comercializacao_service
from apps.backend.app.modules.resources.agricultura.api.schemas.comercializacao_schema import (
    ComercializacaoCreate,
    ComercializacaoResponse,
)
from apps.backend.app.modules.resources.agricultura.application.services.comercializacao_service import (
    ComercializacaoService,
)
from apps.backend.app.modules.resources.agricultura.exceptions import (
    ComercializacaoNotFoundError,
    SafraNotFoundError,
)

router = APIRouter(prefix="/comercializacao", tags=["Agricultura - comercializacao"])
comercializacao_service_dep = Depends(get_comercializacao_service)


@router.post("/", response_model=ComercializacaoResponse, status_code=status.HTTP_201_CREATED)
async def registrar_venda(
    data: ComercializacaoCreate,
    service: ComercializacaoService = comercializacao_service_dep,
):
    try:
        return await service.registrar_venda(
            codigo_safra=data.codigo_safra,
            comprador=data.comprador,
            quantidade_ton=data.quantidade_ton,
            preco_unitario=data.preco_unitario,
        )
    except SafraNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get("/{codigo_comercializacao:path}", response_model=ComercializacaoResponse)
async def obter_venda(
    codigo_comercializacao: str,
    service: ComercializacaoService = comercializacao_service_dep,
):
    try:
        return await service.obter(codigo_comercializacao)
    except ComercializacaoNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.get("/", response_model=list[ComercializacaoResponse])
async def listar_vendas(
    codigo_safra: str | None = None,
    service: ComercializacaoService = comercializacao_service_dep,
):
    return await service.listar(codigo_safra=codigo_safra)
