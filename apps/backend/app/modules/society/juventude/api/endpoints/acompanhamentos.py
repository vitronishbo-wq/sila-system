from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from apps.backend.app.modules.society.juventude.api.deps import get_acompanhamento_juvenil_service
from apps.backend.app.modules.society.juventude.api.schemas.acompanhamento_juvenil_schema import (
    AcompanhamentoJuvenilCreate,
    AcompanhamentoJuvenilEncerrar,
    AcompanhamentoJuvenilEvolucao,
    AcompanhamentoJuvenilResponse,
)
from apps.backend.app.modules.society.juventude.application.services.acompanhamento_juvenil_service import (
    AcompanhamentoJuvenilService,
)
from apps.backend.app.modules.society.juventude.domain.enums import StatusAcompanhamento

router = APIRouter(prefix="/acompanhamentos", tags=["Juventude - Acompanhamentos"])

acompanhamento_juvenil_service_dep = Depends(get_acompanhamento_juvenil_service)


@router.post("/", response_model=AcompanhamentoJuvenilResponse, status_code=status.HTTP_201_CREATED)
async def abrir_acompanhamento(
    data: AcompanhamentoJuvenilCreate,
    service: AcompanhamentoJuvenilService = acompanhamento_juvenil_service_dep,
) -> AcompanhamentoJuvenilResponse:
    try:
        return await service.abrir_acompanhamento(
            jovem_id=data.jovem_id,
            responsavel=data.responsavel,
            objetivo=data.objetivo,
            data_inicio=data.data_inicio,
            proxima_revisao=data.proxima_revisao,
            observacoes=data.observacoes,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get("/{acompanhamento_id}", response_model=AcompanhamentoJuvenilResponse)
async def obter_acompanhamento(
    acompanhamento_id: UUID,
    service: AcompanhamentoJuvenilService = acompanhamento_juvenil_service_dep,
) -> AcompanhamentoJuvenilResponse:
    try:
        return await service.buscar_acompanhamento(acompanhamento_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.get("/", response_model=list[AcompanhamentoJuvenilResponse])
async def listar_acompanhamentos(
    jovem_id: UUID | None = None,
    status_filtro: StatusAcompanhamento | None = None,
    service: AcompanhamentoJuvenilService = acompanhamento_juvenil_service_dep,
) -> list[AcompanhamentoJuvenilResponse]:
    return await service.listar_acompanhamentos(jovem_id=jovem_id, status=status_filtro)


@router.patch("/{acompanhamento_id}/evolucoes", response_model=AcompanhamentoJuvenilResponse)
async def registrar_evolucao(
    acompanhamento_id: UUID,
    data: AcompanhamentoJuvenilEvolucao,
    service: AcompanhamentoJuvenilService = acompanhamento_juvenil_service_dep,
) -> AcompanhamentoJuvenilResponse:
    try:
        return await service.registrar_evolucao(
            acompanhamento_id=acompanhamento_id,
            descricao=data.descricao,
            proxima_revisao=data.proxima_revisao,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.patch("/{acompanhamento_id}/encerrar", response_model=AcompanhamentoJuvenilResponse)
async def encerrar_acompanhamento(
    acompanhamento_id: UUID,
    data: AcompanhamentoJuvenilEncerrar,
    service: AcompanhamentoJuvenilService = acompanhamento_juvenil_service_dep,
) -> AcompanhamentoJuvenilResponse:
    try:
        return await service.encerrar_acompanhamento(
            acompanhamento_id=acompanhamento_id, observacoes=data.observacoes
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.delete("/{acompanhamento_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remover_acompanhamento(
    acompanhamento_id: UUID,
    service: AcompanhamentoJuvenilService = acompanhamento_juvenil_service_dep,
) -> None:
    try:
        await service.remover_acompanhamento(acompanhamento_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc