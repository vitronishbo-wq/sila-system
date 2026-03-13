from __future__ import annotations
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from apps.backend.app.modules.resources.pecuaria.api.deps import get_producao_service
from apps.backend.app.modules.resources.pecuaria.api.schemas.producao_schema import ProducaoCarneCreate, ProducaoCarneResponse, ProducaoLeiteCreate, ProducaoLeiteResponse
from apps.backend.app.modules.resources.pecuaria.application.services.producao_service import ProducaoService
router = APIRouter(prefix='/producao', tags=['Pecuaria - Producao'])

@router.post('/leite', response_model=ProducaoLeiteResponse, status_code=status.HTTP_201_CREATED)
async def registrar_producao_leite(data: ProducaoLeiteCreate, service: ProducaoService=Depends(get_producao_service)):
    try:
        return await service.registrar_leite(propriedade_id=data.propriedade_id, litros=data.litros, data_producao=data.data_producao)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/carne', response_model=ProducaoCarneResponse, status_code=status.HTTP_201_CREATED)
async def registrar_producao_carne(data: ProducaoCarneCreate, service: ProducaoService=Depends(get_producao_service)):
    try:
        return await service.registrar_carne(propriedade_id=data.propriedade_id, quilos=data.quilos, data_producao=data.data_producao)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.get('/', response_model=list[ProducaoLeiteResponse | ProducaoCarneResponse])
async def listar_producoes(propriedade_id: UUID | None=None, service: ProducaoService=Depends(get_producao_service)):
    return await service.listar(propriedade_id=propriedade_id)