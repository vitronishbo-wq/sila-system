from __future__ import annotations
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from apps.backend.app.modules.intelligence.ciencia_pesquisa.api.deps import get_projeto_pesquisa_service
from apps.backend.app.modules.intelligence.ciencia_pesquisa.api.schemas.projeto_pesquisa_schema import ProjetoPesquisaCreate, ProjetoPesquisaEncerrarInput, ProjetoPesquisaResponse, ProjetoPesquisaVincularPesquisadoresInput
from apps.backend.app.modules.intelligence.ciencia_pesquisa.application.services.projeto_pesquisa_service import ProjetoPesquisaService
router = APIRouter(prefix='/projetos', tags=['Ciencia Pesquisa - Projetos'])

def _status_code_for_error(message: str) -> int:
    normalized = message.lower()
    if 'nao encontrado' in normalized:
        return status.HTTP_404_NOT_FOUND
    return status.HTTP_400_BAD_REQUEST

@router.post('/', response_model=ProjetoPesquisaResponse, status_code=status.HTTP_201_CREATED)
async def cadastrar_projeto(data: ProjetoPesquisaCreate, service: ProjetoPesquisaService=Depends(get_projeto_pesquisa_service)) -> ProjetoPesquisaResponse:
    try:
        return await service.cadastrar_projeto(titulo=data.titulo, resumo=data.resumo, instituicao_id=data.instituicao_id, coordenador_id=data.coordenador_id, equipe_pesquisadores_ids=data.equipe_pesquisadores_ids, area_conhecimento=data.area_conhecimento, data_inicio=data.data_inicio, data_fim_prevista=data.data_fim_prevista, palavras_chave=data.palavras_chave, orcamento_previsto=data.orcamento_previsto, codigo_projeto=data.codigo_projeto)
    except ValueError as exc:
        raise HTTPException(status_code=_status_code_for_error(str(exc)), detail=str(exc))

@router.get('/{projeto_id}', response_model=ProjetoPesquisaResponse)
async def obter_projeto(projeto_id: UUID, service: ProjetoPesquisaService=Depends(get_projeto_pesquisa_service)) -> ProjetoPesquisaResponse:
    try:
        return await service.buscar_projeto(projeto_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.get('/', response_model=list[ProjetoPesquisaResponse])
async def listar_projetos(instituicao_id: UUID | None=None, pesquisador_id: UUID | None=None, service: ProjetoPesquisaService=Depends(get_projeto_pesquisa_service)) -> list[ProjetoPesquisaResponse]:
    return await service.listar_projetos(instituicao_id=instituicao_id, pesquisador_id=pesquisador_id)

@router.patch('/{projeto_id}/vincular-pesquisadores', response_model=ProjetoPesquisaResponse)
async def vincular_pesquisadores(projeto_id: UUID, data: ProjetoPesquisaVincularPesquisadoresInput, service: ProjetoPesquisaService=Depends(get_projeto_pesquisa_service)) -> ProjetoPesquisaResponse:
    try:
        return await service.vincular_pesquisadores(projeto_id=projeto_id, pesquisador_ids=data.pesquisador_ids)
    except ValueError as exc:
        raise HTTPException(status_code=_status_code_for_error(str(exc)), detail=str(exc))

@router.patch('/{projeto_id}/aprovar', response_model=ProjetoPesquisaResponse)
async def aprovar_projeto(projeto_id: UUID, service: ProjetoPesquisaService=Depends(get_projeto_pesquisa_service)) -> ProjetoPesquisaResponse:
    try:
        return await service.aprovar_projeto(projeto_id)
    except ValueError as exc:
        raise HTTPException(status_code=_status_code_for_error(str(exc)), detail=str(exc))

@router.patch('/{projeto_id}/iniciar-execucao', response_model=ProjetoPesquisaResponse)
async def iniciar_execucao_projeto(projeto_id: UUID, service: ProjetoPesquisaService=Depends(get_projeto_pesquisa_service)) -> ProjetoPesquisaResponse:
    try:
        return await service.iniciar_execucao_projeto(projeto_id)
    except ValueError as exc:
        raise HTTPException(status_code=_status_code_for_error(str(exc)), detail=str(exc))

@router.patch('/{projeto_id}/suspender', response_model=ProjetoPesquisaResponse)
async def suspender_projeto(projeto_id: UUID, service: ProjetoPesquisaService=Depends(get_projeto_pesquisa_service)) -> ProjetoPesquisaResponse:
    try:
        return await service.suspender_projeto(projeto_id)
    except ValueError as exc:
        raise HTTPException(status_code=_status_code_for_error(str(exc)), detail=str(exc))

@router.patch('/{projeto_id}/encerrar', response_model=ProjetoPesquisaResponse)
async def encerrar_projeto(projeto_id: UUID, data: ProjetoPesquisaEncerrarInput, service: ProjetoPesquisaService=Depends(get_projeto_pesquisa_service)) -> ProjetoPesquisaResponse:
    try:
        return await service.encerrar_projeto(projeto_id=projeto_id, data_fim_real=data.data_fim_real)
    except ValueError as exc:
        raise HTTPException(status_code=_status_code_for_error(str(exc)), detail=str(exc))

@router.delete('/{projeto_id}', status_code=status.HTTP_204_NO_CONTENT)
async def remover_projeto(projeto_id: UUID, service: ProjetoPesquisaService=Depends(get_projeto_pesquisa_service)) -> None:
    try:
        await service.remover_projeto(projeto_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))