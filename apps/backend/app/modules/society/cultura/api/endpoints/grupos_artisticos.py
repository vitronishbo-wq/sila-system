from __future__ import annotations
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from apps.backend.app.modules.society.cultura.api.deps import get_grupo_artistico_service
from apps.backend.app.modules.society.cultura.api.schemas.grupo_artistico_schema import GrupoArtisticoCreate, GrupoArtisticoResponse, GrupoArtisticoUpdate
from apps.backend.app.modules.society.cultura.application.services.grupo_artistico_service import GrupoArtisticoService
from apps.backend.app.modules.society.cultura.domain.enums import TipoGrupoArtistico
router = APIRouter(prefix='/grupos-artisticos', tags=['Cultura - Grupos Artisticos'])

@router.post('/', response_model=GrupoArtisticoResponse, status_code=status.HTTP_201_CREATED)
async def cadastrar_grupo(data: GrupoArtisticoCreate, service: GrupoArtisticoService=Depends(get_grupo_artistico_service)) -> GrupoArtisticoResponse:
    try:
        return await service.cadastrar_grupo(nome=data.nome, tipo=data.tipo, lider_artista_id=data.lider_artista_id, descricao=data.descricao, data_fundacao=data.data_fundacao, municipio=data.municipio, provincia=data.provincia, instituicao_educacional_id=data.instituicao_educacional_id, membros_ids=data.membros_ids, observacoes=data.observacoes)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.get('/{grupo_id}', response_model=GrupoArtisticoResponse)
async def obter_grupo(grupo_id: UUID, service: GrupoArtisticoService=Depends(get_grupo_artistico_service)) -> GrupoArtisticoResponse:
    try:
        return await service.buscar_grupo(grupo_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.get('/', response_model=list[GrupoArtisticoResponse])
async def listar_grupos(tipo: TipoGrupoArtistico | None=None, municipio: str | None=None, somente_ativos: bool=True, service: GrupoArtisticoService=Depends(get_grupo_artistico_service)) -> list[GrupoArtisticoResponse]:
    return await service.listar_grupos(tipo=tipo, municipio=municipio, somente_ativos=somente_ativos)

@router.patch('/{grupo_id}', response_model=GrupoArtisticoResponse)
async def atualizar_grupo(grupo_id: UUID, data: GrupoArtisticoUpdate, service: GrupoArtisticoService=Depends(get_grupo_artistico_service)) -> GrupoArtisticoResponse:
    try:
        return await service.atualizar_grupo(grupo_id=grupo_id, nome=data.nome, tipo=data.tipo, lider_artista_id=data.lider_artista_id, descricao=data.descricao, data_fundacao=data.data_fundacao, municipio=data.municipio, provincia=data.provincia, instituicao_educacional_id=data.instituicao_educacional_id, membros_ids=data.membros_ids, ativo=data.ativo, observacoes=data.observacoes)
    except ValueError as exc:
        message = str(exc).lower()
        code = status.HTTP_404_NOT_FOUND if 'nao encontrado' in message else status.HTTP_400_BAD_REQUEST
        raise HTTPException(status_code=code, detail=str(exc))

@router.delete('/{grupo_id}', status_code=status.HTTP_204_NO_CONTENT)
async def remover_grupo(grupo_id: UUID, service: GrupoArtisticoService=Depends(get_grupo_artistico_service)) -> None:
    try:
        await service.remover_grupo(grupo_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))