from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException, status
from apps.backend.app.modules.resources.ambiente.api.deps import get_penalidade_service
from apps.backend.app.modules.resources.ambiente.api.schemas.multa_schema import MultaCancelamentoInput, MultaCreate, MultaParcelamentoInput, MultaResponse
from apps.backend.app.modules.resources.ambiente.application.services.penalidade_service import PenalidadeService
from apps.backend.app.modules.resources.ambiente.domain.enums import StatusMulta
from apps.backend.app.modules.resources.ambiente.exceptions import AutoInfracaoNotFoundError, MultaNotFoundError
router = APIRouter(prefix='/multas', tags=['Ambiente - Multas'])

@router.post('/', response_model=MultaResponse, status_code=status.HTTP_201_CREATED)
async def aplicar_multa(data: MultaCreate, service: PenalidadeService=Depends(get_penalidade_service)):
    try:
        return await service.aplicar_multa(numero_auto_infracao=data.numero_auto_infracao, valor=data.valor, dias_vencimento=data.dias_vencimento)
    except AutoInfracaoNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/{numero_multa:path}/parcelar', response_model=MultaResponse)
async def parcelar_multa(numero_multa: str, data: MultaParcelamentoInput, service: PenalidadeService=Depends(get_penalidade_service)):
    try:
        return await service.parcelar_multa(numero_multa, quantidade_parcelas=data.quantidade_parcelas)
    except MultaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/{numero_multa:path}/pagar', response_model=MultaResponse)
async def pagar_multa(numero_multa: str, service: PenalidadeService=Depends(get_penalidade_service)):
    try:
        return await service.registrar_pagamento_multa(numero_multa)
    except MultaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/{numero_multa:path}/cancelar', response_model=MultaResponse)
async def cancelar_multa(numero_multa: str, data: MultaCancelamentoInput, service: PenalidadeService=Depends(get_penalidade_service)):
    try:
        return await service.cancelar_multa(numero_multa, motivo=data.motivo)
    except MultaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.get('/{numero_multa:path}', response_model=MultaResponse)
async def obter_multa(numero_multa: str, service: PenalidadeService=Depends(get_penalidade_service)):
    try:
        return await service.obter_multa_por_numero(numero_multa)
    except MultaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.get('/', response_model=list[MultaResponse])
async def listar_multas(numero_auto_infracao: str | None=None, status_multa: StatusMulta | None=None, service: PenalidadeService=Depends(get_penalidade_service)):
    return await service.listar_multas(numero_auto_infracao=numero_auto_infracao, status=status_multa)