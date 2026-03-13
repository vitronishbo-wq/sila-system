from __future__ import annotations
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from app.modules.logistics.api.deps import get_viagem_service
from app.modules.logistics.api.schemas.viagem_schema import ViagemCancelarInput, ViagemConcluirInput, ViagemCreate, ViagemResponse
from app.modules.logistics.application.services import ViagemService
from app.modules.logistics.domain.enums import StatusViagem
from app.modules.logistics.core.exceptions import InvalidViagemStateError, ViagemConflictError, ViagemNotFoundError
router = APIRouter(prefix='/viagens', tags=['Transportes Logistica - Viagens'])

@router.post('/', response_model=ViagemResponse, status_code=status.HTTP_201_CREATED)
async def programar_viagem(data: ViagemCreate, service: ViagemService=Depends(get_viagem_service)):
    try:
        return await service.programar_viagem(linha_id=data.linha_id, veiculo_id=data.veiculo_id, motorista_id=data.motorista_id, data_hora_saida=data.data_hora_saida, data_hora_chegada_prevista=data.data_hora_chegada_prevista, origem=data.origem, destino=data.destino, itinerario=data.itinerario, observacoes=data.observacoes)
    except ViagemConflictError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/{viagem_id}/iniciar', response_model=ViagemResponse)
async def iniciar_viagem(viagem_id: UUID, service: ViagemService=Depends(get_viagem_service)):
    try:
        return await service.iniciar_viagem(viagem_id)
    except ViagemNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except InvalidViagemStateError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/{viagem_id}/concluir', response_model=ViagemResponse)
async def concluir_viagem(viagem_id: UUID, data: ViagemConcluirInput, service: ViagemService=Depends(get_viagem_service)):
    try:
        return await service.concluir_viagem(viagem_id, data_hora_chegada=data.data_hora_chegada)
    except ViagemNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except InvalidViagemStateError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/{viagem_id}/cancelar', response_model=ViagemResponse)
async def cancelar_viagem(viagem_id: UUID, data: ViagemCancelarInput, service: ViagemService=Depends(get_viagem_service)):
    try:
        return await service.cancelar_viagem(viagem_id, motivo=data.motivo)
    except ViagemNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except InvalidViagemStateError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.get('/{viagem_id}', response_model=ViagemResponse)
async def obter_viagem(viagem_id: UUID, service: ViagemService=Depends(get_viagem_service)):
    try:
        return await service.obter_por_id(viagem_id)
    except ViagemNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.get('/', response_model=list[ViagemResponse])
async def listar_viagens(status_viagem: StatusViagem | None=None, linha_id: UUID | None=None, veiculo_id: UUID | None=None, service: ViagemService=Depends(get_viagem_service)):
    return await service.listar(status=status_viagem, linha_id=linha_id, veiculo_id=veiculo_id)
