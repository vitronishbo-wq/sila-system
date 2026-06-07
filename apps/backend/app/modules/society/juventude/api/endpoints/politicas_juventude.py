from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from apps.backend.app.modules.society.juventude.api.deps import get_politica_juventude_service
from apps.backend.app.modules.society.juventude.api.schemas.politica_juventude_schema import (
    PoliticaJuventudeCreate,
    PoliticaJuventudeResponse,
    PoliticaJuventudeStatusUpdate,
)
from apps.backend.app.modules.society.juventude.application.services.politica_juventude_service import (
    PoliticaJuventudeService,
)
from apps.backend.app.modules.society.juventude.domain.enums import (
    AreaInteresse,
    StatusPoliticaJuventude,
)

router = APIRouter(prefix="/politicas-juventude", tags=["Juventude - Politicas"])

politica_juventude_service_dep = Depends(get_politica_juventude_service)


@router.post("/", response_model=PoliticaJuventudeResponse, status_code=status.HTTP_201_CREATED)
async def criar_politica(
    data: PoliticaJuventudeCreate,
    service: PoliticaJuventudeService = politica_juventude_service_dep,
) -> PoliticaJuventudeResponse:
    try:
        return await service.criar_politica(
            nome=data.nome,
            descricao=data.descricao,
            area_interesse=data.area_interesse,
            data_inicio=data.data_inicio,
            metas=data.metas,
            indicadores=data.indicadores,
            data_fim=data.data_fim,
            observacoes=data.observacoes,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get("/{politica_id}", response_model=PoliticaJuventudeResponse)
async def obter_politica(
    politica_id: UUID, service: PoliticaJuventudeService = politica_juventude_service_dep
) -> PoliticaJuventudeResponse:
    try:
        return await service.buscar_politica(politica_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.get("/", response_model=list[PoliticaJuventudeResponse])
async def listar_politicas(
    status_filtro: StatusPoliticaJuventude | None = None,
    area_filtro: AreaInteresse | None = None,
    service: PoliticaJuventudeService = politica_juventude_service_dep,
) -> list[PoliticaJuventudeResponse]:
    return await service.listar_politicas(status=status_filtro, area=area_filtro)


@router.patch("/{politica_id}/status", response_model=PoliticaJuventudeResponse)
async def atualizar_status_politica(
    politica_id: UUID,
    data: PoliticaJuventudeStatusUpdate,
    service: PoliticaJuventudeService = politica_juventude_service_dep,
) -> PoliticaJuventudeResponse:
    try:
        return await service.atualizar_status(politica_id=politica_id, status=data.status)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.delete("/{politica_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remover_politica(
    politica_id: UUID, service: PoliticaJuventudeService = politica_juventude_service_dep
) -> None:
    try:
        await service.remover_politica(politica_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc