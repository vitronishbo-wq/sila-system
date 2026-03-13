from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException, status
from app.modules.resources.agricultura.api.deps import get_credito_service
from app.modules.resources.agricultura.api.schemas.credito_schema import CreditoAprovacaoInput, CreditoCreate, CreditoResponse
from app.modules.resources.agricultura.application.services.credito_service import CreditoService
from app.modules.resources.agricultura.exceptions import CreditoNotFoundError
router = APIRouter(prefix='/creditos', tags=['Agricultura - creditos'])

@router.post('/', response_model=CreditoResponse, status_code=status.HTTP_201_CREATED)
async def solicitar_credito(data: CreditoCreate, service: CreditoService=Depends(get_credito_service)):
    try:
        return await service.solicitar(codigo_produtor=data.codigo_produtor, finalidade=data.finalidade, valor_solicitado=data.valor_solicitado)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/{codigo_credito:path}/aprovar', response_model=CreditoResponse)
async def aprovar_credito(codigo_credito: str, data: CreditoAprovacaoInput, service: CreditoService=Depends(get_credito_service)):
    try:
        return await service.aprovar(codigo_credito, valor_aprovado=data.valor_aprovado)
    except CreditoNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/{codigo_credito:path}/desembolsar', response_model=CreditoResponse)
async def desembolsar_credito(codigo_credito: str, service: CreditoService=Depends(get_credito_service)):
    try:
        return await service.desembolsar(codigo_credito)
    except CreditoNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.get('/{codigo_credito:path}', response_model=CreditoResponse)
async def obter_credito(codigo_credito: str, service: CreditoService=Depends(get_credito_service)):
    try:
        return await service.obter(codigo_credito)
    except CreditoNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.get('/', response_model=list[CreditoResponse])
async def listar_creditos(codigo_produtor: str | None=None, service: CreditoService=Depends(get_credito_service)):
    return await service.listar(codigo_produtor=codigo_produtor)