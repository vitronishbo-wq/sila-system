from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from apps.backend.app.modules.society.desporto.api.deps import get_estadio_service
from apps.backend.app.modules.society.desporto.api.schemas.estadio_schema import (
    EstadioCreate,
    EstadioResponse,
    EstadioUpdate,
)
from apps.backend.app.modules.society.desporto.application.services.estadio_service import (
    EstadioService,
)

router = APIRouter(prefix="/estadios", tags=["Desporto - Estadios"])

estadio_service_dep = Depends(get_estadio_service)


@router.post("/", response_model=EstadioResponse, status_code=status.HTTP_201_CREATED)
async def cadastrar_estadio(
    data: EstadioCreate, service: EstadioService = estadio_service_dep
) -> EstadioResponse:
    try:
        return await service.cadastrar_estadio(
            nome=data.nome,
            tipo=data.tipo,
            municipio=data.municipio,
            provincia=data.provincia,
            capacidade=data.capacidade,
            estado_relvado=data.estado_relvado,
            codigo_obra_instalacao=data.codigo_obra_instalacao,
            clube_mandante_id=data.clube_mandante_id,
            observacoes=data.observacoes,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get("/{estadio_id}", response_model=EstadioResponse)
async def obter_estadio(
    estadio_id: UUID, service: EstadioService = estadio_service_dep
) -> EstadioResponse:
    try:
        return await service.buscar_estadio(estadio_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.get("/", response_model=list[EstadioResponse])
async def listar_estadios(
    municipio: str | None = None,
    somente_ativos: bool = True,
    service: EstadioService = estadio_service_dep,
) -> list[EstadioResponse]:
    return await service.listar_estadios(municipio=municipio, somente_ativos=somente_ativos)


@router.patch("/{estadio_id}", response_model=EstadioResponse)
async def atualizar_estadio(
    estadio_id: UUID, data: EstadioUpdate, service: EstadioService = estadio_service_dep
) -> EstadioResponse:
    try:
        return await service.atualizar_estadio(
            estadio_id=estadio_id,
            nome=data.nome,
            tipo=data.tipo,
            municipio=data.municipio,
            provincia=data.provincia,
            capacidade=data.capacidade,
            estado_relvado=data.estado_relvado,
            codigo_obra_instalacao=data.codigo_obra_instalacao,
            clube_mandante_id=data.clube_mandante_id,
            ativo=data.ativo,
            observacoes=data.observacoes,
        )
    except ValueError as exc:
        message = str(exc).lower()
        code = (
            status.HTTP_404_NOT_FOUND
            if "nao encontrado" in message
            else status.HTTP_400_BAD_REQUEST
        )
        raise HTTPException(status_code=code, detail=str(exc)) from exc


@router.delete("/{estadio_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remover_estadio(
    estadio_id: UUID, service: EstadioService = estadio_service_dep
) -> None:
    try:
        await service.remover_estadio(estadio_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc