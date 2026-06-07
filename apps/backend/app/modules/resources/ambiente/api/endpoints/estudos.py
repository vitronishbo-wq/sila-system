from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from apps.backend.app.modules.resources.ambiente.api.deps import get_estudo_service
from apps.backend.app.modules.resources.ambiente.api.schemas.estudo_schema import (
    EstudoAprovacaoInput,
    EstudoComplementacaoInput,
    EstudoCreate,
    EstudoResponse,
)
from apps.backend.app.modules.resources.ambiente.application.services.estudo_service import (
    EstudoService,
)
from apps.backend.app.modules.resources.ambiente.domain.enums import (
    StatusEstudoAmbiental,
    TipoEstudoAmbiental,
)
from apps.backend.app.modules.resources.ambiente.exceptions import (
    EstudoNotFoundError,
    LicencaNotFoundError,
)

router = APIRouter(prefix="/estudos", tags=["Ambiente - Estudos"])

estudo_service_dep = Depends(get_estudo_service)


@router.post("/", response_model=EstudoResponse, status_code=status.HTTP_201_CREATED)
async def submeter_estudo(data: EstudoCreate, service: EstudoService = estudo_service_dep):
    try:
        return await service.submeter(
            numero_licenca=data.numero_licenca,
            tipo=data.tipo,
            descricao=data.descricao,
            responsavel_tecnico=data.responsavel_tecnico,
        )
    except LicencaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/{numero_estudo:path}/analise", response_model=EstudoResponse)
async def iniciar_analise_estudo(
    numero_estudo: str, service: EstudoService = estudo_service_dep
):
    try:
        return await service.iniciar_analise(numero_estudo)
    except EstudoNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/{numero_estudo:path}/aprovar", response_model=EstudoResponse)
async def aprovar_estudo(
    numero_estudo: str,
    data: EstudoAprovacaoInput,
    service: EstudoService = estudo_service_dep,
):
    try:
        return await service.aprovar(numero_estudo, data.analista_id)
    except EstudoNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/{numero_estudo:path}/complementacao", response_model=EstudoResponse)
async def solicitar_complementacao_estudo(
    numero_estudo: str,
    data: EstudoComplementacaoInput,
    service: EstudoService = estudo_service_dep,
):
    try:
        return await service.solicitar_complementacao(numero_estudo, data.analista_id, data.motivo)
    except EstudoNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get("/{numero_estudo:path}", response_model=EstudoResponse)
async def obter_estudo(numero_estudo: str, service: EstudoService = estudo_service_dep):
    try:
        return await service.obter_por_numero(numero_estudo)
    except EstudoNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.get("/", response_model=list[EstudoResponse])
async def listar_estudos(
    numero_licenca: str | None = None,
    tipo: TipoEstudoAmbiental | None = None,
    status_estudo: StatusEstudoAmbiental | None = None,
    service: EstudoService = estudo_service_dep,
):
    return await service.listar(numero_licenca=numero_licenca, tipo=tipo, status=status_estudo)