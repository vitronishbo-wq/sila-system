from __future__ import annotations
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from apps.backend.app.modules.governance.cooperacao_internacional.api.deps import get_visto_service
from apps.backend.app.modules.governance.cooperacao_internacional.api.schemas.visto_schema import VistoAnaliseInput, VistoAprovarInput, VistoCreate, VistoNegarInput, VistoResponse
from apps.backend.app.modules.governance.cooperacao_internacional.application.services.visto_service import VistoService
router = APIRouter(prefix='/vistos', tags=['Cooperacao Internacional - Vistos'])

@router.post('/', response_model=VistoResponse, status_code=status.HTTP_201_CREATED)
async def solicitar_visto(payload: VistoCreate, service: VistoService=Depends(get_visto_service)) -> VistoResponse:
    try:
        visto = await service.solicitar_visto(**payload.model_dump())
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    return VistoResponse.model_validate(visto)

@router.post('/{visto_id}/analisar', response_model=VistoResponse)
async def analisar_visto(visto_id: UUID, payload: VistoAnaliseInput, service: VistoService=Depends(get_visto_service)) -> VistoResponse:
    try:
        visto = await service.analisar_visto(visto_id=visto_id, **payload.model_dump())
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    return VistoResponse.model_validate(visto)

@router.post('/{visto_id}/aprovar', response_model=VistoResponse)
async def aprovar_visto(visto_id: UUID, payload: VistoAprovarInput, service: VistoService=Depends(get_visto_service)) -> VistoResponse:
    try:
        visto = await service.aprovar_visto(visto_id=visto_id, **payload.model_dump())
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    return VistoResponse.model_validate(visto)

@router.post('/{visto_id}/emitir', response_model=VistoResponse)
async def emitir_visto(visto_id: UUID, service: VistoService=Depends(get_visto_service)) -> VistoResponse:
    try:
        visto = await service.emitir_visto(visto_id=visto_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    return VistoResponse.model_validate(visto)

@router.post('/{visto_id}/negar', response_model=VistoResponse)
async def negar_visto(visto_id: UUID, payload: VistoNegarInput, service: VistoService=Depends(get_visto_service)) -> VistoResponse:
    try:
        visto = await service.negar_visto(visto_id=visto_id, motivo=payload.motivo)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    return VistoResponse.model_validate(visto)

@router.get('/', response_model=list[VistoResponse])
async def listar_vistos(service: VistoService=Depends(get_visto_service)) -> list[VistoResponse]:
    vistos = await service.listar_vistos()
    return [VistoResponse.model_validate(item) for item in vistos]