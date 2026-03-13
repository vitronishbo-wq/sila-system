from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException, status
from app.modules.resources.agricultura.api.deps import get_operacao_service
from app.modules.resources.agricultura.api.schemas.operacao_schema import OperacaoCreate, OperacaoResponse
from app.modules.resources.agricultura.application.services.operacao_service import OperacaoService
from app.modules.resources.agricultura.exceptions import InsumoNotFoundError, OperacaoNotFoundError, SafraNotFoundError
router = APIRouter(prefix='/operacoes', tags=['Agricultura - operacoes'])

@router.post('/', response_model=OperacaoResponse, status_code=status.HTTP_201_CREATED)
async def registrar_operacao(data: OperacaoCreate, service: OperacaoService=Depends(get_operacao_service)):
    try:
        return await service.registrar_operacao(codigo_safra=data.codigo_safra, tipo=data.tipo, descricao=data.descricao, codigo_insumo=data.codigo_insumo, quantidade_insumo=data.quantidade_insumo)
    except (SafraNotFoundError, InsumoNotFoundError) as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.get('/{codigo_operacao:path}', response_model=OperacaoResponse)
async def obter_operacao(codigo_operacao: str, service: OperacaoService=Depends(get_operacao_service)):
    try:
        return await service.obter(codigo_operacao)
    except OperacaoNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.get('/', response_model=list[OperacaoResponse])
async def listar_operacoes(codigo_safra: str | None=None, service: OperacaoService=Depends(get_operacao_service)):
    return await service.listar(codigo_safra=codigo_safra)