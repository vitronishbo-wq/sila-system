from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from apps.backend.app.modules.society.cultura.api.deps import get_artista_service
from apps.backend.app.modules.society.cultura.api.schemas.artista_schema import (
    ArtistaCreate,
    ArtistaResponse,
    ArtistaUpdate,
)
from apps.backend.app.modules.society.cultura.application.services.artista_service import (
    ArtistaService,
)
from apps.backend.app.modules.society.cultura.domain.enums import TipoArtista

router = APIRouter(prefix="/artistas", tags=["Cultura - Artistas"])

artista_service_dep = Depends(get_artista_service)


@router.post("/", response_model=ArtistaResponse, status_code=status.HTTP_201_CREATED)
async def cadastrar_artista(
    data: ArtistaCreate, service: ArtistaService = artista_service_dep
) -> ArtistaResponse:
    try:
        return await service.cadastrar_artista(
            nome=data.nome,
            tipo=data.tipo,
            citizen_id=data.citizen_id,
            nome_artistico=data.nome_artistico,
            data_nascimento=data.data_nascimento,
            naturalidade=data.naturalidade,
            nacionalidade=data.nacionalidade,
            biografia=data.biografia,
            municipio=data.municipio,
            provincia=data.provincia,
            observacoes=data.observacoes,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get("/{artista_id}", response_model=ArtistaResponse)
async def obter_artista(
    artista_id: UUID, service: ArtistaService = artista_service_dep
) -> ArtistaResponse:
    try:
        return await service.buscar_artista(artista_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.get("/", response_model=list[ArtistaResponse])
async def listar_artistas(
    tipo: TipoArtista | None = None,
    somente_ativos: bool = True,
    service: ArtistaService = artista_service_dep,
) -> list[ArtistaResponse]:
    return await service.listar_artistas(tipo=tipo, somente_ativos=somente_ativos)


@router.patch("/{artista_id}", response_model=ArtistaResponse)
async def atualizar_artista(
    artista_id: UUID, data: ArtistaUpdate, service: ArtistaService = artista_service_dep
) -> ArtistaResponse:
    try:
        return await service.atualizar_artista(
            artista_id=artista_id,
            nome=data.nome,
            tipo=data.tipo,
            nome_artistico=data.nome_artistico,
            data_nascimento=data.data_nascimento,
            naturalidade=data.naturalidade,
            nacionalidade=data.nacionalidade,
            biografia=data.biografia,
            municipio=data.municipio,
            provincia=data.provincia,
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


@router.delete("/{artista_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remover_artista(
    artista_id: UUID, service: ArtistaService = artista_service_dep
) -> None:
    try:
        await service.remover_artista(artista_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc