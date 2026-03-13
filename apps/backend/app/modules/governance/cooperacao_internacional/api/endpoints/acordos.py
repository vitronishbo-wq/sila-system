from __future__ import annotations
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, status
from apps.backend.app.modules.governance.cooperacao_internacional.api.deps import get_acordo_service
from apps.backend.app.modules.governance.cooperacao_internacional.api.schemas.acordo_schema import AcordoAssinarInput, AcordoCreate, AcordoRatificarInput, AcordoResponse, AcordoVigorInput
from apps.backend.app.modules.governance.cooperacao_internacional.application.services.acordo_service import AcordoService
router = APIRouter(prefix='/acordos', tags=['Cooperacao Internacional - Acordos'])

@router.post('/', response_model=AcordoResponse, status_code=status.HTTP_201_CREATED)
async def criar_acordo(payload: AcordoCreate, service: AcordoService=Depends(get_acordo_service)) -> AcordoResponse:
    try:
        acordo = await service.criar_acordo(**payload.model_dump())
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    return AcordoResponse.model_validate(acordo)

@router.get('/', response_model=list[AcordoResponse])
async def listar_acordos(service: AcordoService=Depends(get_acordo_service)) -> list[AcordoResponse]:
    acordos = await service.listar_acordos()
    return [AcordoResponse.model_validate(item) for item in acordos]

@router.post('/{acordo_id}/assinar', response_model=AcordoResponse)
async def assinar_acordo(acordo_id: UUID, payload: AcordoAssinarInput, service: AcordoService=Depends(get_acordo_service)) -> AcordoResponse:
    try:
        acordo = await service.assinar_acordo(acordo_id=acordo_id, partes=payload.model_dump()['partes'], local_assinatura=payload.local_assinatura)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    return AcordoResponse.model_validate(acordo)

@router.post('/{acordo_id}/ratificar', response_model=AcordoResponse)
async def ratificar_acordo(acordo_id: UUID, payload: AcordoRatificarInput, service: AcordoService=Depends(get_acordo_service)) -> AcordoResponse:
    try:
        acordo = await service.ratificar_acordo(acordo_id=acordo_id, **payload.model_dump())
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    return AcordoResponse.model_validate(acordo)

@router.post('/{acordo_id}/vigor', response_model=AcordoResponse)
async def iniciar_vigor_acordo(acordo_id: UUID, payload: AcordoVigorInput, service: AcordoService=Depends(get_acordo_service)) -> AcordoResponse:
    try:
        acordo = await service.iniciar_vigor(acordo_id=acordo_id, data_vigor=payload.data_vigor)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    return AcordoResponse.model_validate(acordo)

@router.get('/vencimento/proximo')
async def acordos_vencimento_proximo(dias: int=Query(90, ge=1, le=3650), service: AcordoService=Depends(get_acordo_service)) -> list[dict]:
    return await service.get_acordos_vencimento_proximo(dias=dias)