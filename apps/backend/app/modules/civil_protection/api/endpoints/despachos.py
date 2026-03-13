from __future__ import annotations
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from apps.backend.app.modules.civil_protection.api.deps import get_despacho_service
from apps.backend.app.modules.civil_protection.api.schemas.despacho_schema import DespachoCreate, DespachoResponse, DespachoStatusUpdate
from apps.backend.app.modules.civil_protection.application.services.despacho_service import DespachoService
from apps.backend.app.modules.civil_protection.domain.enums import StatusDespacho
router = APIRouter(prefix='/despachos', tags=['Protecao Civil - Despachos'])

@router.post('/', response_model=DespachoResponse, status_code=status.HTTP_201_CREATED)
async def registrar_despacho(data: DespachoCreate, service: DespachoService=Depends(get_despacho_service)) -> DespachoResponse:
    try:
        return await service.registrar_despacho(ocorrencia_id=data.ocorrencia_id, bombeiro_responsavel_id=data.bombeiro_responsavel_id, meio_deslocamento=data.meio_deslocamento, observacoes=data.observacoes, citizen_id=data.citizen_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.get('/{despacho_id}', response_model=DespachoResponse)
async def obter_despacho(despacho_id: UUID, service: DespachoService=Depends(get_despacho_service)) -> DespachoResponse:
    try:
        return await service.buscar_despacho(despacho_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.get('/', response_model=list[DespachoResponse])
async def listar_despachos(ocorrencia_id: UUID | None=None, status_despacho: StatusDespacho | None=None, service: DespachoService=Depends(get_despacho_service)) -> list[DespachoResponse]:
    return await service.listar_despachos(ocorrencia_id=ocorrencia_id, status=status_despacho)

@router.patch('/{despacho_id}/status', response_model=DespachoResponse)
async def atualizar_status_despacho(despacho_id: UUID, data: DespachoStatusUpdate, service: DespachoService=Depends(get_despacho_service)) -> DespachoResponse:
    try:
        return await service.atualizar_status(despacho_id=despacho_id, status=data.status, observacoes=data.observacoes)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.delete('/{despacho_id}', status_code=status.HTTP_204_NO_CONTENT)
async def remover_despacho(despacho_id: UUID, service: DespachoService=Depends(get_despacho_service)) -> None:
    try:
        await service.remover_despacho(despacho_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))