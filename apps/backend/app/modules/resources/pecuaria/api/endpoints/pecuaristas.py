from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from apps.backend.app.modules.resources.pecuaria.api.deps import get_pecuarista_service
from apps.backend.app.modules.resources.pecuaria.api.schemas.pecuarista_schema import (
    PecuaristaAtivarInput,
    PecuaristaCreate,
    PecuaristaFilter,
    PecuaristaResponse,
)
from apps.backend.app.modules.resources.pecuaria.application.services.pecuarista_service import (
    PecuaristaService,
)

router = APIRouter(prefix="/pecuaristas", tags=["Pecuaria - Pecuaristas"])

pecuarista_service_dep = Depends(get_pecuarista_service)
filtros_dep = Depends()


@router.post("/", response_model=PecuaristaResponse, status_code=status.HTTP_201_CREATED)
async def cadastrar_pecuarista(
    data: PecuaristaCreate, service: PecuaristaService = pecuarista_service_dep
):
    try:
        return await service.cadastrar_pecuarista(
            nome=data.nome,
            documento=data.documento,
            documento_tipo=data.documento_tipo,
            telefone=data.telefone,
            email=data.email,
            endereco=data.endereco,
            citizen_id=data.citizen_id,
            empresa_id=data.empresa_id,
            observacoes=data.observacoes,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/{cadastro_pecuarista:path}/ativar", response_model=PecuaristaResponse)
async def ativar_pecuarista(
    cadastro_pecuarista: str,
    data: PecuaristaAtivarInput,
    service: PecuaristaService = pecuarista_service_dep,
):
    try:
        return await service.ativar_pecuarista(cadastro_pecuarista, actor_id=data.actor_id)
    except ValueError as exc:
        detail = str(exc)
        code = (
            status.HTTP_404_NOT_FOUND
            if "nao encontrado" in detail.lower()
            else status.HTTP_400_BAD_REQUEST
        )
        raise HTTPException(status_code=code, detail=detail) from exc


@router.get("/{cadastro_pecuarista:path}", response_model=PecuaristaResponse)
async def obter_pecuarista(
    cadastro_pecuarista: str, service: PecuaristaService = pecuarista_service_dep
):
    item = await service.obter_por_cadastro(cadastro_pecuarista)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Pecuarista nao encontrado"
        )
    return item


@router.get("/", response_model=list[PecuaristaResponse])
async def listar_pecuaristas(
    filtros: PecuaristaFilter = filtros_dep,
    service: PecuaristaService = pecuarista_service_dep,
):
    return await service.listar(status=filtros.status)
