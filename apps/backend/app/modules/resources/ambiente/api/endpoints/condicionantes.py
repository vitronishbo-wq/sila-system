from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from apps.backend.app.modules.resources.ambiente.api.deps import get_condicionante_service
from apps.backend.app.modules.resources.ambiente.api.schemas.condicionante_schema import (
    CondicionanteCreate,
    CondicionanteCumprimentoInput,
    CondicionanteDescumprimentoInput,
    CondicionanteResponse,
)
from apps.backend.app.modules.resources.ambiente.application.services.condicionante_service import (
    CondicionanteService,
)
from apps.backend.app.modules.resources.ambiente.domain.enums import StatusCondicionante
from apps.backend.app.modules.resources.ambiente.exceptions import (
    CondicionanteNotFoundError,
    LicencaNotFoundError,
)

router = APIRouter(prefix="/condicionantes", tags=["Ambiente - Condicionantes"])

condicionante_service_dep = Depends(get_condicionante_service)


@router.post("/", response_model=CondicionanteResponse, status_code=status.HTTP_201_CREATED)
async def criar_condicionante(
    data: CondicionanteCreate, service: CondicionanteService = condicionante_service_dep
):
    try:
        return await service.criar(
            numero_licenca=data.numero_licenca, descricao=data.descricao, prazo_dias=data.prazo_dias
        )
    except LicencaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/{codigo_condicionante:path}/iniciar", response_model=CondicionanteResponse)
async def iniciar_cumprimento(
    codigo_condicionante: str, service: CondicionanteService = condicionante_service_dep
):
    try:
        return await service.iniciar_cumprimento(codigo_condicionante)
    except CondicionanteNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/{codigo_condicionante:path}/concluir", response_model=CondicionanteResponse)
async def concluir_condicionante(
    codigo_condicionante: str,
    data: CondicionanteCumprimentoInput,
    service: CondicionanteService = condicionante_service_dep,
):
    try:
        return await service.registrar_cumprimento(codigo_condicionante, data.evidencia)
    except CondicionanteNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/{codigo_condicionante:path}/descumprir", response_model=CondicionanteResponse)
async def descumprir_condicionante(
    codigo_condicionante: str,
    data: CondicionanteDescumprimentoInput,
    service: CondicionanteService = condicionante_service_dep,
):
    try:
        return await service.marcar_descumprimento(codigo_condicionante, data.motivo)
    except CondicionanteNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get("/{codigo_condicionante:path}", response_model=CondicionanteResponse)
async def obter_condicionante(
    codigo_condicionante: str, service: CondicionanteService = condicionante_service_dep
):
    try:
        return await service.obter_por_codigo(codigo_condicionante)
    except CondicionanteNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.get("/", response_model=list[CondicionanteResponse])
async def listar_condicionantes(
    numero_licenca: str | None = None,
    status_condicionante: StatusCondicionante | None = None,
    service: CondicionanteService = condicionante_service_dep,
):
    return await service.listar(numero_licenca=numero_licenca, status=status_condicionante)