from __future__ import annotations
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from app.modules.resources.pescas.industrial.api.deps import get_unidade_processamento_service
from app.modules.resources.pescas.industrial.api.schemas.unidade_processamento_schema import UnidadeProcessamentoCreate, UnidadeProcessamentoResponse, UnidadeProcessamentoUpdateCapacidade
from app.modules.resources.pescas.industrial.application.services.unidade_processamento_service import UnidadeProcessamentoService
from app.modules.resources.pescas.industrial.domain.enums import TipoProcessamento
router = APIRouter(prefix='/unidades-processamento', tags=['Pescas Industriais - Unidades de Processamento'])

@router.post('/', response_model=UnidadeProcessamentoResponse, status_code=status.HTTP_201_CREATED)
async def cadastrar_unidade(data: UnidadeProcessamentoCreate, service: UnidadeProcessamentoService=Depends(get_unidade_processamento_service)) -> UnidadeProcessamentoResponse:
    try:
        return await service.cadastrar_unidade(cnpj=data.cnpj, razao_social=data.razao_social, tipo_processamento=data.tipo_processamento, classificacao=data.classificacao, capacidade_kg_dia=data.capacidade_kg_dia, area_total_m2=data.area_total_m2, area_producao_m2=data.area_producao_m2, area_armazenagem_m2=data.area_armazenagem_m2, numero_funcionarios=data.numero_funcionarios, endereco=data.endereco, municipio=data.municipio, provincia=data.provincia, armador_id=data.armador_id, responsavel_tecnico_id=data.responsavel_tecnico_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.get('/{unidade_id}', response_model=UnidadeProcessamentoResponse)
async def obter_unidade(unidade_id: UUID, service: UnidadeProcessamentoService=Depends(get_unidade_processamento_service)) -> UnidadeProcessamentoResponse:
    try:
        return await service.buscar_unidade(unidade_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.get('/', response_model=list[UnidadeProcessamentoResponse])
async def listar_unidades(municipio: str | None=None, tipo: TipoProcessamento | None=None, service: UnidadeProcessamentoService=Depends(get_unidade_processamento_service)) -> list[UnidadeProcessamentoResponse]:
    if tipo is not None:
        return await service.listar_unidades_por_tipo(tipo)
    return await service.listar_unidades(municipio)

@router.patch('/{unidade_id}/capacidade', response_model=UnidadeProcessamentoResponse)
async def atualizar_capacidade(unidade_id: UUID, data: UnidadeProcessamentoUpdateCapacidade, service: UnidadeProcessamentoService=Depends(get_unidade_processamento_service)) -> UnidadeProcessamentoResponse:
    try:
        return await service.atualizar_capacidade(unidade_id, data.capacidade_kg_dia)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.delete('/{unidade_id}', status_code=status.HTTP_204_NO_CONTENT)
async def remover_unidade(unidade_id: UUID, service: UnidadeProcessamentoService=Depends(get_unidade_processamento_service)) -> None:
    try:
        await service.remover_unidade(unidade_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))