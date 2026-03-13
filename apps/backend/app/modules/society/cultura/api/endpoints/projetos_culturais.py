from __future__ import annotations
from datetime import date
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from app.modules.society.cultura.api.deps import get_projeto_cultural_service
from app.modules.society.cultura.api.schemas.projeto_cultural_schema import ProjetoAprovacaoRequest, ProjetoCulturalCreate, ProjetoCulturalResponse, ProjetoCulturalUpdate, ProjetoExecucaoRequest
from app.modules.society.cultura.application.services.projeto_cultural_service import ProjetoCulturalService
from app.modules.society.cultura.domain.enums import StatusProjetoCultural, TipoProjetoCultural
router = APIRouter(prefix='/projetos-culturais', tags=['Cultura - Projetos Culturais'])

@router.post('/', response_model=ProjetoCulturalResponse, status_code=status.HTTP_201_CREATED)
async def cadastrar_projeto(data: ProjetoCulturalCreate, service: ProjetoCulturalService=Depends(get_projeto_cultural_service)) -> ProjetoCulturalResponse:
    try:
        return await service.cadastrar_projeto(titulo=data.titulo, tipo=data.tipo, natureza=data.natureza, proponente_cpf_cnpj=data.proponente_cpf_cnpj, proponente_nome=data.proponente_nome, resumo=data.resumo, valor_solicitado=data.valor_solicitado, justificativa=data.justificativa, edital_id=data.edital_id, objetivos=data.objetivos, observacoes=data.observacoes, submeter=data.submeter)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.get('/{projeto_id}', response_model=ProjetoCulturalResponse)
async def obter_projeto(projeto_id: UUID, service: ProjetoCulturalService=Depends(get_projeto_cultural_service)) -> ProjetoCulturalResponse:
    try:
        return await service.buscar_projeto(projeto_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.get('/', response_model=list[ProjetoCulturalResponse])
async def listar_projetos(tipo: TipoProjetoCultural | None=None, status_projeto: StatusProjetoCultural | None=None, data_inicio: date | None=None, data_fim: date | None=None, somente_ativos: bool=True, service: ProjetoCulturalService=Depends(get_projeto_cultural_service)) -> list[ProjetoCulturalResponse]:
    return await service.listar_projetos(tipo=tipo, status=status_projeto, data_inicio=data_inicio, data_fim=data_fim, somente_ativos=somente_ativos)

@router.patch('/{projeto_id}', response_model=ProjetoCulturalResponse)
async def atualizar_projeto(projeto_id: UUID, data: ProjetoCulturalUpdate, service: ProjetoCulturalService=Depends(get_projeto_cultural_service)) -> ProjetoCulturalResponse:
    try:
        return await service.atualizar_projeto(projeto_id=projeto_id, titulo=data.titulo, tipo=data.tipo, natureza=data.natureza, resumo=data.resumo, valor_solicitado=data.valor_solicitado, justificativa=data.justificativa, objetivos=data.objetivos, ativo=data.ativo, observacoes=data.observacoes)
    except ValueError as exc:
        message = str(exc).lower()
        code = status.HTTP_404_NOT_FOUND if 'nao encontrado' in message else status.HTTP_400_BAD_REQUEST
        raise HTTPException(status_code=code, detail=str(exc))

@router.patch('/{projeto_id}/aprovar', response_model=ProjetoCulturalResponse)
async def aprovar_projeto(projeto_id: UUID, data: ProjetoAprovacaoRequest, service: ProjetoCulturalService=Depends(get_projeto_cultural_service)) -> ProjetoCulturalResponse:
    try:
        return await service.aprovar_projeto(projeto_id=projeto_id, valor_aprovado=data.valor_aprovado)
    except ValueError as exc:
        message = str(exc).lower()
        code = status.HTTP_404_NOT_FOUND if 'nao encontrado' in message else status.HTTP_400_BAD_REQUEST
        raise HTTPException(status_code=code, detail=str(exc))

@router.patch('/{projeto_id}/reprovar', response_model=ProjetoCulturalResponse)
async def reprovar_projeto(projeto_id: UUID, service: ProjetoCulturalService=Depends(get_projeto_cultural_service)) -> ProjetoCulturalResponse:
    try:
        return await service.reprovar_projeto(projeto_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.patch('/{projeto_id}/iniciar', response_model=ProjetoCulturalResponse)
async def iniciar_execucao(projeto_id: UUID, data: ProjetoExecucaoRequest, service: ProjetoCulturalService=Depends(get_projeto_cultural_service)) -> ProjetoCulturalResponse:
    try:
        return await service.iniciar_execucao(projeto_id=projeto_id, data_inicio=data.data)
    except ValueError as exc:
        message = str(exc).lower()
        code = status.HTTP_404_NOT_FOUND if 'nao encontrado' in message else status.HTTP_400_BAD_REQUEST
        raise HTTPException(status_code=code, detail=str(exc))

@router.patch('/{projeto_id}/concluir', response_model=ProjetoCulturalResponse)
async def concluir_projeto(projeto_id: UUID, data: ProjetoExecucaoRequest, service: ProjetoCulturalService=Depends(get_projeto_cultural_service)) -> ProjetoCulturalResponse:
    try:
        return await service.concluir_projeto(projeto_id=projeto_id, data_fim=data.data)
    except ValueError as exc:
        message = str(exc).lower()
        code = status.HTTP_404_NOT_FOUND if 'nao encontrado' in message else status.HTTP_400_BAD_REQUEST
        raise HTTPException(status_code=code, detail=str(exc))

@router.delete('/{projeto_id}', status_code=status.HTTP_204_NO_CONTENT)
async def remover_projeto(projeto_id: UUID, service: ProjetoCulturalService=Depends(get_projeto_cultural_service)) -> None:
    try:
        await service.remover_projeto(projeto_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))