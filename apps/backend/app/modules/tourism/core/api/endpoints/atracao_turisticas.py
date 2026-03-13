from __future__ import annotations
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from app.modules.tourism.api.deps import get_atracao_service
from app.modules.tourism.api.schemas.atracao_turistica_schema import AtracaoTuristicaCreate, AtracaoTuristicaResponse, AtracaoTuristicaUpdate
from app.modules.tourism.application.services.atracao_service import AtracaoService
from app.modules.tourism.domain.enums import TipoAtracao
router = APIRouter(prefix='/atracoes-turisticas', tags=['Turismo - Atracoes Turisticas'])

@router.post('/', response_model=AtracaoTuristicaResponse, status_code=status.HTTP_201_CREATED)
async def cadastrar_atracao(data: AtracaoTuristicaCreate, service: AtracaoService=Depends(get_atracao_service)) -> AtracaoTuristicaResponse:
    try:
        return await service.cadastrar(nome=data.nome, tipo=data.tipo, descricao=data.descricao, endereco=data.endereco, municipio=data.municipio, provincia=data.provincia, horario_funcionamento=data.horario_funcionamento, acessivel=data.acessivel, gratuita=data.gratuita, capacidade_visitantes_dia=data.capacidade_visitantes_dia, valor_entrada=data.valor_entrada, latitude=data.latitude, longitude=data.longitude, observacoes=data.observacoes)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.get('/{atracao_id}', response_model=AtracaoTuristicaResponse)
async def obter_atracao(atracao_id: UUID, service: AtracaoService=Depends(get_atracao_service)) -> AtracaoTuristicaResponse:
    try:
        return await service.obter(atracao_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.get('/', response_model=list[AtracaoTuristicaResponse])
async def listar_atracoes(tipo: TipoAtracao | None=None, municipio: str | None=None, ativa: bool | None=None, service: AtracaoService=Depends(get_atracao_service)) -> list[AtracaoTuristicaResponse]:
    return await service.listar(tipo=tipo, municipio=municipio, ativa=ativa)

@router.put('/{atracao_id}', response_model=AtracaoTuristicaResponse)
async def atualizar_atracao(atracao_id: UUID, data: AtracaoTuristicaUpdate, service: AtracaoService=Depends(get_atracao_service)) -> AtracaoTuristicaResponse:
    try:
        return await service.atualizar(atracao_id, nome=data.nome, tipo=data.tipo, descricao=data.descricao, endereco=data.endereco, municipio=data.municipio, provincia=data.provincia, horario_funcionamento=data.horario_funcionamento, acessivel=data.acessivel, gratuita=data.gratuita, capacidade_visitantes_dia=data.capacidade_visitantes_dia, valor_entrada=data.valor_entrada, latitude=data.latitude, longitude=data.longitude, observacoes=data.observacoes, ativa=data.ativa)
    except ValueError as exc:
        status_code = status.HTTP_404_NOT_FOUND if 'nao encontrada' in str(exc).lower() else status.HTTP_400_BAD_REQUEST
        raise HTTPException(status_code=status_code, detail=str(exc))

@router.delete('/{atracao_id}', status_code=status.HTTP_204_NO_CONTENT)
async def remover_atracao(atracao_id: UUID, service: AtracaoService=Depends(get_atracao_service)) -> None:
    try:
        await service.remover(atracao_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
