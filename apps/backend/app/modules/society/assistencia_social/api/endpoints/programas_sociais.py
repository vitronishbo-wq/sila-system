from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, status

from apps.backend.app.modules.society.assistencia_social.api.deps import get_programa_social_service
from apps.backend.app.modules.society.assistencia_social.api.endpoints._errors import (
    raise_http_for_value_error,
)
from apps.backend.app.modules.society.assistencia_social.api.schemas.programa_social_schema import (
    ProgramaSocialCreate,
    ProgramaSocialEncerrar,
    ProgramaSocialResponse,
    ProgramaSocialSuspender,
)
from apps.backend.app.modules.society.assistencia_social.application.services.programa_social_service import (
    ProgramaSocialService,
)

router = APIRouter(prefix="/programas-sociais", tags=["Assistencia Social - Programas"])

programa_social_service_dep = Depends(get_programa_social_service)


@router.post("/", response_model=ProgramaSocialResponse, status_code=status.HTTP_201_CREATED)
async def criar_programa_social(
    data: ProgramaSocialCreate,
    service: ProgramaSocialService = programa_social_service_dep,
) -> ProgramaSocialResponse:
    return await service.criar_programa(
        nome=data.nome,
        publico_alvo=data.publico_alvo,
        criterio_renda_max=data.criterio_renda_max,
        valor_base=data.valor_base,
        vagas=data.vagas,
        data_inicio=data.data_inicio,
        observacoes=data.observacoes,
    )


@router.get("/{programa_id}", response_model=ProgramaSocialResponse)
async def obter_programa_social(
    programa_id: UUID, service: ProgramaSocialService = programa_social_service_dep
) -> ProgramaSocialResponse:
    try:
        return await service.buscar_programa(programa_id)
    except ValueError as exc:
        raise_http_for_value_error(exc)


@router.get("/", response_model=list[ProgramaSocialResponse])
async def listar_programas_sociais(
    service: ProgramaSocialService = programa_social_service_dep,
) -> list[ProgramaSocialResponse]:
    return await service.listar_programas()


@router.patch("/{programa_id}/ativar", response_model=ProgramaSocialResponse)
async def ativar_programa_social(
    programa_id: UUID, service: ProgramaSocialService = programa_social_service_dep
) -> ProgramaSocialResponse:
    try:
        return await service.ativar_programa(programa_id)
    except ValueError as exc:
        raise_http_for_value_error(exc)


@router.patch("/{programa_id}/suspender", response_model=ProgramaSocialResponse)
async def suspender_programa_social(
    programa_id: UUID,
    data: ProgramaSocialSuspender,
    service: ProgramaSocialService = programa_social_service_dep,
) -> ProgramaSocialResponse:
    try:
        return await service.suspender_programa(programa_id, data.motivo)
    except ValueError as exc:
        raise_http_for_value_error(exc)


@router.patch("/{programa_id}/encerrar", response_model=ProgramaSocialResponse)
async def encerrar_programa_social(
    programa_id: UUID,
    data: ProgramaSocialEncerrar,
    service: ProgramaSocialService = programa_social_service_dep,
) -> ProgramaSocialResponse:
    try:
        return await service.encerrar_programa(
            programa_id, data_fim=data.data_fim, motivo=data.motivo
        )
    except ValueError as exc:
        raise_http_for_value_error(exc)


@router.delete("/{programa_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remover_programa_social(
    programa_id: UUID, service: ProgramaSocialService = programa_social_service_dep
) -> None:
    try:
        await service.remover_programa(programa_id)
    except ValueError as exc:
        raise_http_for_value_error(exc)