from __future__ import annotations
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, status
from apps.backend.app.modules.resources.pescas.api.deps import get_captura_service
from apps.backend.app.modules.resources.pescas.api.schemas.captura_schema import CapturaCreate, CapturaResponse
from apps.backend.app.modules.resources.pescas.application.services.captura_service import CapturaService
router = APIRouter(prefix='/capturas', tags=['Pescas - Capturas'])

@router.post('/', response_model=CapturaResponse, status_code=status.HTTP_201_CREATED)
async def registrar_captura(data: CapturaCreate, service: CapturaService=Depends(get_captura_service)):
    try:
        return await service.registrar_captura(embarcacao_id=data.embarcacao_id, licenca_id=data.licenca_id, zona_pesca_id=data.zona_pesca_id, especie_id=data.especie_id, quantidade_kg=data.quantidade_kg, arte_pesca_id=data.arte_pesca_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.get('/{captura_id}', response_model=CapturaResponse)
async def obter_captura(captura_id: UUID, service: CapturaService=Depends(get_captura_service)):
    try:
        return await service.buscar_captura(captura_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.get('/', response_model=list[CapturaResponse])
async def listar_capturas(embarcacao_id: UUID=Query(...), service: CapturaService=Depends(get_captura_service)):
    return await service.listar_capturas(embarcacao_id)