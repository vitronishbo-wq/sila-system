from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID
from app.modules.resources.agricultura.api.deps import get_propriedade_service
from app.modules.resources.agricultura.api.schemas.propriedade_schema import PropriedadeCreate, PropriedadeResponse
from app.modules.resources.agricultura.application.services.propriedade_service import PropriedadeService
from app.modules.resources.agricultura.exceptions import PropriedadeNotFoundError
router = APIRouter(prefix='/propriedades', tags=['Agricultura - propriedades'])

@router.post('/', response_model=PropriedadeResponse, status_code=status.HTTP_201_CREATED)
async def cadastrar_propriedade(data: PropriedadeCreate, service: PropriedadeService=Depends(get_propriedade_service)):
    try:
        return await service.cadastrar(produtor_id=data.produtor_id, nome=data.nome, tipo=data.tipo, area_total_ha=data.area_total_ha, area_cultivavel_ha=data.area_cultivavel_ha, provincia=data.provincia, municipio=data.municipio)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.get('/{codigo_propriedade:path}', response_model=PropriedadeResponse)
async def obter_propriedade(codigo_propriedade: str, service: PropriedadeService=Depends(get_propriedade_service)):
    try:
        return await service.obter(codigo_propriedade)
    except PropriedadeNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.get('/', response_model=list[PropriedadeResponse])
async def listar_propriedades(produtor_id: UUID | None=None, service: PropriedadeService=Depends(get_propriedade_service)):
    return await service.listar(produtor_id=produtor_id)