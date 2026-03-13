from __future__ import annotations
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from app.modules.public_security.api.deps import get_vestigio_service
from app.modules.public_security.api.schemas.vestigio_schema import VestigioCreate, VestigioResponse, VestigioStatusUpdate
from app.modules.public_security.application.services.vestigio_service import VestigioService
from app.modules.public_security.domain.enums import StatusVestigio
router = APIRouter(prefix='/vestigios', tags=['Seguranca Publica - Vestigios'])

@router.post('/', response_model=VestigioResponse, status_code=status.HTTP_201_CREATED)
async def registrar_vestigio(data: VestigioCreate, service: VestigioService=Depends(get_vestigio_service)) -> VestigioResponse:
    try:
        return await service.registrar_vestigio(cadeia_custodia_id=data.cadeia_custodia_id, tipo=data.tipo, descricao=data.descricao, localizacao=data.localizacao, coletado_por_id=data.coletado_por_id, observacoes=data.observacoes, citizen_id=data.citizen_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.get('/{vestigio_id}', response_model=VestigioResponse)
async def obter_vestigio(vestigio_id: UUID, service: VestigioService=Depends(get_vestigio_service)) -> VestigioResponse:
    try:
        return await service.buscar_vestigio(vestigio_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.get('/', response_model=list[VestigioResponse])
async def listar_vestigios(cadeia_custodia_id: UUID | None=None, status_vestigio: StatusVestigio | None=None, service: VestigioService=Depends(get_vestigio_service)) -> list[VestigioResponse]:
    return await service.listar_vestigios(cadeia_custodia_id=cadeia_custodia_id, status=status_vestigio)

@router.patch('/{vestigio_id}/status', response_model=VestigioResponse)
async def atualizar_status_vestigio(vestigio_id: UUID, data: VestigioStatusUpdate, service: VestigioService=Depends(get_vestigio_service)) -> VestigioResponse:
    try:
        return await service.atualizar_status(vestigio_id=vestigio_id, status=data.status, observacoes=data.observacoes)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.delete('/{vestigio_id}', status_code=status.HTTP_204_NO_CONTENT)
async def remover_vestigio(vestigio_id: UUID, service: VestigioService=Depends(get_vestigio_service)) -> None:
    try:
        await service.remover_vestigio(vestigio_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))