from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from apps.backend.app.modules.energy.api.deps import get_linha_transmissao_service
from apps.backend.app.modules.energy.api.schemas.linha_transmissao_schema import (
    LinhaTransmissaoCreate,
    LinhaTransmissaoDataInput,
    LinhaTransmissaoResponse,
)
from apps.backend.app.modules.energy.application.services import LinhaTransmissaoService
from apps.backend.app.modules.energy.domain.enums import StatusInfraEnergia
from apps.backend.app.modules.energy.domain.exceptions import (
    InvalidLinhaTransmissaoStateError,
    LinhaTransmissaoNotFoundError,
)

router = APIRouter(prefix="/linha_transmissao", tags=["Energia - Linha Transmissao"])

linha_transmissao_service_dep = Depends(get_linha_transmissao_service)


@router.post("/", response_model=LinhaTransmissaoResponse, status_code=status.HTTP_201_CREATED)
async def cadastrar(
    data: LinhaTransmissaoCreate,
    service: LinhaTransmissaoService = linha_transmissao_service_dep,
):
    try:
        return await service.cadastrar(
            origem_id=data.origem_id,
            origem_tipo=data.origem_tipo,
            destino_id=data.destino_id,
            destino_tipo=data.destino_tipo,
            capacidade_mw=data.capacidade_mw,
            extensao_km=data.extensao_km,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.patch("/{id}/iniciar_construcao", response_model=LinhaTransmissaoResponse)
async def iniciar_construcao(
    id: UUID,
    data: LinhaTransmissaoDataInput,
    service: LinhaTransmissaoService = linha_transmissao_service_dep,
):
    try:
        return await service.iniciar_construcao(id, data_inicio=data.data)
    except LinhaTransmissaoNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except InvalidLinhaTransmissaoStateError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.patch("/{id}/iniciar_operacao", response_model=LinhaTransmissaoResponse)
async def iniciar_operacao(
    id: UUID,
    data: LinhaTransmissaoDataInput,
    service: LinhaTransmissaoService = linha_transmissao_service_dep,
):
    try:
        return await service.iniciar_operacao(id, data_operacao=data.data)
    except LinhaTransmissaoNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except InvalidLinhaTransmissaoStateError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get("/", response_model=list[LinhaTransmissaoResponse])
async def listar(
    status_item: StatusInfraEnergia | None = None,
    service: LinhaTransmissaoService = linha_transmissao_service_dep,
):
    return await service.listar(status=status_item)