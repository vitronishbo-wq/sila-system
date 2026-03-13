from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException, status
from apps.backend.app.modules.resources.agricultura.api.deps import get_insumo_service
from apps.backend.app.modules.resources.agricultura.api.schemas.insumo_schema import InsumoCreate, InsumoResponse, MovimentoInsumoInput
from apps.backend.app.modules.resources.agricultura.application.services.insumo_service import InsumoService
from apps.backend.app.modules.resources.agricultura.exceptions import InsumoNotFoundError
router = APIRouter(prefix='/insumos', tags=['Agricultura - insumos'])

@router.post('/', response_model=InsumoResponse, status_code=status.HTTP_201_CREATED)
async def cadastrar_insumo(data: InsumoCreate, service: InsumoService=Depends(get_insumo_service)):
    try:
        return await service.cadastrar(nome=data.nome, tipo=data.tipo, unidade_medida=data.unidade_medida, quantidade_inicial=data.quantidade_inicial, custo_unitario=data.custo_unitario)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/{codigo_insumo:path}/entrada', response_model=InsumoResponse)
async def registrar_entrada(codigo_insumo: str, data: MovimentoInsumoInput, service: InsumoService=Depends(get_insumo_service)):
    try:
        return await service.registrar_entrada(codigo_insumo, data.quantidade)
    except InsumoNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/{codigo_insumo:path}/baixa', response_model=InsumoResponse)
async def registrar_baixa(codigo_insumo: str, data: MovimentoInsumoInput, service: InsumoService=Depends(get_insumo_service)):
    try:
        return await service.registrar_baixa(codigo_insumo, data.quantidade)
    except InsumoNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.get('/{codigo_insumo:path}', response_model=InsumoResponse)
async def obter_insumo(codigo_insumo: str, service: InsumoService=Depends(get_insumo_service)):
    try:
        return await service.obter(codigo_insumo)
    except InsumoNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.get('/', response_model=list[InsumoResponse])
async def listar_insumos(service: InsumoService=Depends(get_insumo_service)):
    return await service.listar()