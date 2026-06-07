from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from apps.backend.app.modules.society.cultura.api.deps import get_bem_cultural_service
from apps.backend.app.modules.society.cultura.api.schemas.bem_cultural_schema import (
    BemCulturalCreate,
    BemCulturalResponse,
    BemCulturalUpdate,
)
from apps.backend.app.modules.society.cultura.application.services.bem_cultural_service import (
    BemCulturalService,
)
from apps.backend.app.modules.society.cultura.domain.enums import StatusTombamento, TipoPatrimonio

router = APIRouter(prefix="/bens-culturais", tags=["Cultura - Bens Culturais"])

bem_cultural_service_dep = Depends(get_bem_cultural_service)


@router.post("/", response_model=BemCulturalResponse, status_code=status.HTTP_201_CREATED)
async def cadastrar_bem(
    data: BemCulturalCreate, service: BemCulturalService = bem_cultural_service_dep
) -> BemCulturalResponse:
    try:
        return await service.cadastrar_bem(
            nome=data.nome,
            tipo=data.tipo,
            descricao=data.descricao,
            localizacao=data.localizacao,
            municipio=data.municipio,
            provincia=data.provincia,
            coordenadas_lat=data.coordenadas_lat,
            coordenadas_long=data.coordenadas_long,
            observacoes=data.observacoes,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get("/{bem_id}", response_model=BemCulturalResponse)
async def obter_bem(
    bem_id: UUID, service: BemCulturalService = bem_cultural_service_dep
) -> BemCulturalResponse:
    try:
        return await service.buscar_bem(bem_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.get("/", response_model=list[BemCulturalResponse])
async def listar_bens(
    tipo: TipoPatrimonio | None = None,
    municipio: str | None = None,
    status_tombamento: StatusTombamento | None = None,
    somente_ativos: bool = True,
    service: BemCulturalService = bem_cultural_service_dep,
) -> list[BemCulturalResponse]:
    return await service.listar_bens(
        tipo=tipo,
        municipio=municipio,
        status_tombamento=status_tombamento,
        somente_ativos=somente_ativos,
    )


@router.patch("/{bem_id}", response_model=BemCulturalResponse)
async def atualizar_bem(
    bem_id: UUID,
    data: BemCulturalUpdate,
    service: BemCulturalService = bem_cultural_service_dep,
) -> BemCulturalResponse:
    try:
        return await service.atualizar_bem(
            bem_id=bem_id,
            nome=data.nome,
            tipo=data.tipo,
            descricao=data.descricao,
            localizacao=data.localizacao,
            municipio=data.municipio,
            provincia=data.provincia,
            coordenadas_lat=data.coordenadas_lat,
            coordenadas_long=data.coordenadas_long,
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


@router.patch("/{bem_id}/tombar", response_model=BemCulturalResponse)
async def tombar_bem(
    bem_id: UUID, service: BemCulturalService = bem_cultural_service_dep
) -> BemCulturalResponse:
    try:
        return await service.tombar_bem(bem_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.delete("/{bem_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remover_bem(
    bem_id: UUID, service: BemCulturalService = bem_cultural_service_dep
) -> None:
    try:
        await service.remover_bem(bem_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc