from __future__ import annotations
from datetime import date
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from apps.backend.app.modules.society.desporto.api.deps import get_competicao_service
from apps.backend.app.modules.society.desporto.api.schemas.competicao_schema import CompeticaoCreate, CompeticaoResponse, CompeticaoUpdate
from apps.backend.app.modules.society.desporto.application.services.competicao_service import CompeticaoService
from apps.backend.app.modules.society.desporto.domain.enums import ModalidadeDesportiva, StatusCompeticao, TipoCompeticao
router = APIRouter(prefix='/competicoes', tags=['Desporto - Competicoes'])

@router.post('/', response_model=CompeticaoResponse, status_code=status.HTTP_201_CREATED)
async def cadastrar_competicao(data: CompeticaoCreate, service: CompeticaoService=Depends(get_competicao_service)) -> CompeticaoResponse:
    try:
        return await service.cadastrar_competicao(nome=data.nome, tipo=data.tipo, modalidade=data.modalidade, data_inicio=data.data_inicio, data_fim=data.data_fim, municipio=data.municipio, provincia=data.provincia, organizador_id=data.organizador_id, codigo_obra_instalacao=data.codigo_obra_instalacao, atracao_turistica_id=data.atracao_turistica_id, instituicao_educacional_id=data.instituicao_educacional_id, premiacao_total=data.premiacao_total, observacoes=data.observacoes)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.get('/{competicao_id}', response_model=CompeticaoResponse)
async def obter_competicao(competicao_id: UUID, service: CompeticaoService=Depends(get_competicao_service)) -> CompeticaoResponse:
    try:
        return await service.buscar_competicao(competicao_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.get('/', response_model=list[CompeticaoResponse])
async def listar_competicoes(tipo: TipoCompeticao | None=None, modalidade: ModalidadeDesportiva | None=None, status_filtro: StatusCompeticao | None=None, data_inicio: date | None=None, data_fim: date | None=None, somente_ativas: bool=True, service: CompeticaoService=Depends(get_competicao_service)) -> list[CompeticaoResponse]:
    return await service.listar_competicoes(tipo=tipo, modalidade=modalidade, status=status_filtro, data_inicio=data_inicio, data_fim=data_fim, somente_ativas=somente_ativas)

@router.patch('/{competicao_id}', response_model=CompeticaoResponse)
async def atualizar_competicao(competicao_id: UUID, data: CompeticaoUpdate, service: CompeticaoService=Depends(get_competicao_service)) -> CompeticaoResponse:
    try:
        return await service.atualizar_competicao(competicao_id=competicao_id, nome=data.nome, tipo=data.tipo, modalidade=data.modalidade, data_inicio=data.data_inicio, data_fim=data.data_fim, municipio=data.municipio, provincia=data.provincia, codigo_obra_instalacao=data.codigo_obra_instalacao, atracao_turistica_id=data.atracao_turistica_id, instituicao_educacional_id=data.instituicao_educacional_id, premiacao_total=data.premiacao_total, inscricoes_abertas=data.inscricoes_abertas, status=data.status, ativo=data.ativo, observacoes=data.observacoes)
    except ValueError as exc:
        message = str(exc).lower()
        code = status.HTTP_404_NOT_FOUND if 'nao encontrada' in message else status.HTTP_400_BAD_REQUEST
        raise HTTPException(status_code=code, detail=str(exc))

@router.delete('/{competicao_id}', status_code=status.HTTP_204_NO_CONTENT)
async def remover_competicao(competicao_id: UUID, service: CompeticaoService=Depends(get_competicao_service)) -> None:
    try:
        await service.remover_competicao(competicao_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))