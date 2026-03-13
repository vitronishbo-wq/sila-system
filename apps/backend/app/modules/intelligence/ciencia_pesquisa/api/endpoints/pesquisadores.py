from __future__ import annotations
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from apps.backend.app.modules.intelligence.ciencia_pesquisa.api.deps import get_pesquisador_service
from apps.backend.app.modules.intelligence.ciencia_pesquisa.api.schemas.pesquisador_schema import PesquisadorCreate, PesquisadorEncerrarVinculoInput, PesquisadorResponse, PesquisadorVincularInstituicaoInput
from apps.backend.app.modules.intelligence.ciencia_pesquisa.application.services.pesquisador_service import PesquisadorService
router = APIRouter(prefix='/pesquisadores', tags=['Ciencia Pesquisa - Pesquisadores'])

def _status_code_for_error(message: str) -> int:
    normalized = message.lower()
    if 'nao encontrado' in normalized:
        return status.HTTP_404_NOT_FOUND
    return status.HTTP_400_BAD_REQUEST

@router.post('/', response_model=PesquisadorResponse, status_code=status.HTTP_201_CREATED)
async def cadastrar_pesquisador(data: PesquisadorCreate, service: PesquisadorService=Depends(get_pesquisador_service)) -> PesquisadorResponse:
    try:
        return await service.cadastrar_pesquisador(nome_completo=data.nome_completo, documento_identificacao=data.documento_identificacao, email_institucional=data.email_institucional, instituicao_id=data.instituicao_id, unidade_pesquisa_id=data.unidade_pesquisa_id, area_conhecimento=data.area_conhecimento, nivel_formacao=data.nivel_formacao, tipo_vinculo=data.tipo_vinculo, data_inicio_vinculo=data.data_inicio_vinculo, telefone=data.telefone, orcid=data.orcid, lattes_url=data.lattes_url, researcher_id=data.researcher_id, scopus_id=data.scopus_id)
    except ValueError as exc:
        raise HTTPException(status_code=_status_code_for_error(str(exc)), detail=str(exc))

@router.get('/{pesquisador_id}', response_model=PesquisadorResponse)
async def obter_pesquisador(pesquisador_id: UUID, service: PesquisadorService=Depends(get_pesquisador_service)) -> PesquisadorResponse:
    try:
        return await service.buscar_pesquisador(pesquisador_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.get('/', response_model=list[PesquisadorResponse])
async def listar_pesquisadores(instituicao_id: UUID | None=None, service: PesquisadorService=Depends(get_pesquisador_service)) -> list[PesquisadorResponse]:
    return await service.listar_pesquisadores(instituicao_id=instituicao_id)

@router.patch('/{pesquisador_id}/vincular-instituicao', response_model=PesquisadorResponse)
async def vincular_instituicao(pesquisador_id: UUID, data: PesquisadorVincularInstituicaoInput, service: PesquisadorService=Depends(get_pesquisador_service)) -> PesquisadorResponse:
    try:
        return await service.vincular_instituicao(pesquisador_id=pesquisador_id, instituicao_id=data.instituicao_id, unidade_pesquisa_id=data.unidade_pesquisa_id)
    except ValueError as exc:
        raise HTTPException(status_code=_status_code_for_error(str(exc)), detail=str(exc))

@router.patch('/{pesquisador_id}/encerrar-vinculo', response_model=PesquisadorResponse)
async def encerrar_vinculo(pesquisador_id: UUID, data: PesquisadorEncerrarVinculoInput, service: PesquisadorService=Depends(get_pesquisador_service)) -> PesquisadorResponse:
    try:
        return await service.encerrar_vinculo(pesquisador_id=pesquisador_id, data_fim_vinculo=data.data_fim_vinculo)
    except ValueError as exc:
        raise HTTPException(status_code=_status_code_for_error(str(exc)), detail=str(exc))

@router.delete('/{pesquisador_id}', status_code=status.HTTP_204_NO_CONTENT)
async def remover_pesquisador(pesquisador_id: UUID, service: PesquisadorService=Depends(get_pesquisador_service)) -> None:
    try:
        await service.remover_pesquisador(pesquisador_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))