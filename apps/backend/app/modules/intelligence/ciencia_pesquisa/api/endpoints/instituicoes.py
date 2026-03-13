from __future__ import annotations
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from app.modules.intelligence.ciencia_pesquisa.api.deps import get_instituicao_pesquisa_service
from app.modules.intelligence.ciencia_pesquisa.api.schemas.instituicao_pesquisa_schema import InstituicaoPesquisaCreate, InstituicaoPesquisaCredenciarInput, InstituicaoPesquisaResponse
from app.modules.intelligence.ciencia_pesquisa.application.services.instituicao_pesquisa_service import InstituicaoPesquisaService
router = APIRouter(prefix='/instituicoes', tags=['Ciencia Pesquisa - Instituicoes'])

def _status_code_for_error(message: str) -> int:
    normalized = message.lower()
    if 'nao encontrada' in normalized:
        return status.HTTP_404_NOT_FOUND
    return status.HTTP_400_BAD_REQUEST

@router.post('/', response_model=InstituicaoPesquisaResponse, status_code=status.HTTP_201_CREATED)
async def cadastrar_instituicao(data: InstituicaoPesquisaCreate, service: InstituicaoPesquisaService=Depends(get_instituicao_pesquisa_service)) -> InstituicaoPesquisaResponse:
    try:
        return await service.cadastrar_instituicao(sigla=data.sigla, nome=data.nome, nif=data.nif, tipo=data.tipo, natureza_juridica=data.natureza_juridica, pais=data.pais, provincia=data.provincia, municipio=data.municipio, endereco=data.endereco, email_institucional=data.email_institucional, telefone=data.telefone, website=data.website)
    except ValueError as exc:
        raise HTTPException(status_code=_status_code_for_error(str(exc)), detail=str(exc))

@router.get('/{instituicao_id}', response_model=InstituicaoPesquisaResponse)
async def obter_instituicao(instituicao_id: UUID, service: InstituicaoPesquisaService=Depends(get_instituicao_pesquisa_service)) -> InstituicaoPesquisaResponse:
    try:
        return await service.buscar_instituicao(instituicao_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.get('/', response_model=list[InstituicaoPesquisaResponse])
async def listar_instituicoes(somente_ativas: bool=False, service: InstituicaoPesquisaService=Depends(get_instituicao_pesquisa_service)) -> list[InstituicaoPesquisaResponse]:
    return await service.listar_instituicoes(somente_ativas=somente_ativas)

@router.patch('/{instituicao_id}/credenciar', response_model=InstituicaoPesquisaResponse)
async def credenciar_instituicao(instituicao_id: UUID, data: InstituicaoPesquisaCredenciarInput, service: InstituicaoPesquisaService=Depends(get_instituicao_pesquisa_service)) -> InstituicaoPesquisaResponse:
    try:
        return await service.credenciar_instituicao(instituicao_id=instituicao_id, data_credenciamento=data.data_credenciamento, data_validade_credenciamento=data.data_validade_credenciamento)
    except ValueError as exc:
        raise HTTPException(status_code=_status_code_for_error(str(exc)), detail=str(exc))

@router.patch('/{instituicao_id}/suspender', response_model=InstituicaoPesquisaResponse)
async def suspender_instituicao(instituicao_id: UUID, service: InstituicaoPesquisaService=Depends(get_instituicao_pesquisa_service)) -> InstituicaoPesquisaResponse:
    try:
        return await service.suspender_instituicao(instituicao_id)
    except ValueError as exc:
        raise HTTPException(status_code=_status_code_for_error(str(exc)), detail=str(exc))

@router.patch('/{instituicao_id}/descredenciar', response_model=InstituicaoPesquisaResponse)
async def descredenciar_instituicao(instituicao_id: UUID, service: InstituicaoPesquisaService=Depends(get_instituicao_pesquisa_service)) -> InstituicaoPesquisaResponse:
    try:
        return await service.descredenciar_instituicao(instituicao_id)
    except ValueError as exc:
        raise HTTPException(status_code=_status_code_for_error(str(exc)), detail=str(exc))

@router.delete('/{instituicao_id}', status_code=status.HTTP_204_NO_CONTENT)
async def remover_instituicao(instituicao_id: UUID, service: InstituicaoPesquisaService=Depends(get_instituicao_pesquisa_service)) -> None:
    try:
        await service.remover_instituicao(instituicao_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))