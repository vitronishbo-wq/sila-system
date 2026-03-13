from __future__ import annotations
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from apps.backend.app.modules.resources.pecuaria.api.deps import get_propriedade_service
from apps.backend.app.modules.resources.pecuaria.api.schemas.propriedade_schema import PropriedadeCreate, PropriedadeResponse
from apps.backend.app.modules.resources.pecuaria.application.services.propriedade_service import PropriedadeService
router = APIRouter(prefix='/propriedades', tags=['Pecuaria - Propriedades'])

@router.post('/', response_model=PropriedadeResponse, status_code=status.HTTP_201_CREATED)
async def cadastrar_propriedade(data: PropriedadeCreate, service: PropriedadeService=Depends(get_propriedade_service)):
    try:
        return await service.cadastrar(pecuarista_id=data.pecuarista_id, nome=data.nome, area_total_ha=data.area_total_ha, municipio=data.municipio, provincia=data.provincia)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.get('/{codigo_propriedade:path}', response_model=PropriedadeResponse)
async def obter_propriedade(codigo_propriedade: str, service: PropriedadeService=Depends(get_propriedade_service)):
    try:
        return await service.obter(codigo_propriedade)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.get('/', response_model=list[PropriedadeResponse])
async def listar_propriedades(pecuarista_id: UUID | None=None, service: PropriedadeService=Depends(get_propriedade_service)):
    return await service.listar(pecuarista_id=pecuarista_id)