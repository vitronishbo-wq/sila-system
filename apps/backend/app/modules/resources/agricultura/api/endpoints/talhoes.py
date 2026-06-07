from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from apps.backend.app.modules.resources.agricultura.api.deps import get_talhao_service
from apps.backend.app.modules.resources.agricultura.api.schemas.talhao_schema import (
    TalhaoCreate,
    TalhaoResponse,
)
from apps.backend.app.modules.resources.agricultura.application.services.talhao_service import (
    TalhaoService,
)
from apps.backend.app.modules.resources.agricultura.domain.enums import StatusTalhao
from apps.backend.app.modules.resources.agricultura.exceptions import (
    PropriedadeNotFoundError,
    TalhaoNotFoundError,
)

router = APIRouter(prefix="/talhoes", tags=["Agricultura - talhoes"])
talhao_service_dep = Depends(get_talhao_service)


@router.post("/", response_model=TalhaoResponse, status_code=status.HTTP_201_CREATED)
async def cadastrar_talhao(
    data: TalhaoCreate, service: TalhaoService = talhao_service_dep
):
    try:
        return await service.cadastrar(
            codigo_propriedade=data.codigo_propriedade,
            nome=data.nome,
            area_ha=data.area_ha,
            tipo_solo=data.tipo_solo,
            irrigado=data.irrigado,
        )
    except PropriedadeNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/{codigo_talhao:path}/ativar", response_model=TalhaoResponse)
async def ativar_talhao(codigo_talhao: str, service: TalhaoService = talhao_service_dep):
    try:
        return await service.ativar(codigo_talhao)
    except TalhaoNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/{codigo_talhao:path}/desativar", response_model=TalhaoResponse)
async def desativar_talhao(
    codigo_talhao: str, service: TalhaoService = talhao_service_dep
):
    try:
        return await service.desativar(codigo_talhao)
    except TalhaoNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get("/{codigo_talhao:path}", response_model=TalhaoResponse)
async def obter_talhao(codigo_talhao: str, service: TalhaoService = talhao_service_dep):
    try:
        return await service.obter(codigo_talhao)
    except TalhaoNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.get("/", response_model=list[TalhaoResponse])
async def listar_talhoes(
    codigo_propriedade: str | None = None,
    status_talhao: StatusTalhao | None = None,
    service: TalhaoService = talhao_service_dep,
):
    return await service.listar(codigo_propriedade=codigo_propriedade, status=status_talhao)
