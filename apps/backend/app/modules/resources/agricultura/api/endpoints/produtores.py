from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from apps.backend.app.modules.resources.agricultura.api.deps import get_produtor_service
from apps.backend.app.modules.resources.agricultura.api.schemas.produtor_schema import (
    ProdutorAtivarInput,
    ProdutorCreate,
    ProdutorFilter,
    ProdutorResponse,
)
from apps.backend.app.modules.resources.agricultura.application.services.produtor_service import (
    ProdutorService,
)
from apps.backend.app.modules.resources.agricultura.exceptions import (
    CitizenInactiveError,
    ProdutorAlreadyExistsError,
)

router = APIRouter(prefix="/produtores", tags=["Agricultura - Produtores"])
produtor_service_dep = Depends(get_produtor_service)
produtor_filter_dep = Depends()


@router.post("/", response_model=ProdutorResponse, status_code=status.HTTP_201_CREATED)
async def cadastrar_produtor(
    data: ProdutorCreate, service: ProdutorService = produtor_service_dep
):
    try:
        return await service.cadastrar_produtor(
            nome=data.nome,
            documento=data.documento,
            documento_tipo=data.documento_tipo,
            tipo=data.tipo,
            telefone=data.telefone,
            email=data.email,
            endereco=data.endereco,
            citizen_id=data.citizen_id,
            empresa_id=data.empresa_id,
            observacoes=data.observacoes,
        )
    except ProdutorAlreadyExistsError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    except CitizenInactiveError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/{cadastro_produtor:path}/ativar", response_model=ProdutorResponse)
async def ativar_produtor(
    cadastro_produtor: str,
    data: ProdutorAtivarInput,
    service: ProdutorService = produtor_service_dep,
):
    try:
        return await service.ativar_produtor(cadastro_produtor, actor_id=data.actor_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get("/{cadastro_produtor:path}", response_model=ProdutorResponse)
async def obter_produtor(
    cadastro_produtor: str, service: ProdutorService = produtor_service_dep
):
    item = await service.obter_por_cadastro(cadastro_produtor)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produtor nao encontrado")
    return item


@router.get("/", response_model=list[ProdutorResponse])
async def listar_produtores(
    filtros: ProdutorFilter = produtor_filter_dep, service: ProdutorService = produtor_service_dep
):
    return await service.listar(status=filtros.status)
