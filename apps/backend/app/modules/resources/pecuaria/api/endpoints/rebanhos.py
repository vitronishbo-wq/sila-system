from __future__ import annotations
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from app.modules.resources.pecuaria.api.deps import get_rebanho_service
from app.modules.resources.pecuaria.api.schemas.rebanho_schema import RebanhoCreate, RebanhoResponse
from app.modules.resources.pecuaria.application.services.rebanho_service import RebanhoService
router = APIRouter(prefix='/rebanhos', tags=['Pecuaria - Rebanhos'])

@router.post('/', response_model=RebanhoResponse, status_code=status.HTTP_201_CREATED)
async def cadastrar_rebanho(data: RebanhoCreate, service: RebanhoService=Depends(get_rebanho_service)):
    try:
        return await service.cadastrar(propriedade_id=data.propriedade_id, tipo_animal=data.tipo_animal, descricao=data.descricao, quantidade_animais=data.quantidade_animais)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.get('/{codigo_rebanho:path}', response_model=RebanhoResponse)
async def obter_rebanho(codigo_rebanho: str, service: RebanhoService=Depends(get_rebanho_service)):
    try:
        return await service.obter(codigo_rebanho)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.get('/', response_model=list[RebanhoResponse])
async def listar_rebanhos(propriedade_id: UUID | None=None, service: RebanhoService=Depends(get_rebanho_service)):
    return await service.listar(propriedade_id=propriedade_id)