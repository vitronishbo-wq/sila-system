from __future__ import annotations
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from app.modules.energy.api.deps import get_linha_transmissao_service
from app.modules.energy.api.schemas.linha_transmissao_schema import LinhaTransmissaoCreate, LinhaTransmissaoDataInput, LinhaTransmissaoResponse
from app.modules.energy.application.services import LinhaTransmissaoService
from app.modules.energy.domain.enums import StatusInfraEnergia
from app.modules.energy.core.exceptions import InvalidLinhaTransmissaoStateError, LinhaTransmissaoNotFoundError
router = APIRouter(prefix='/linha_transmissao', tags=['Energia - Linha Transmissao'])

@router.post('/', response_model=LinhaTransmissaoResponse, status_code=status.HTTP_201_CREATED)
async def cadastrar(data: LinhaTransmissaoCreate, service: LinhaTransmissaoService=Depends(get_linha_transmissao_service)):
    try:
        return await service.cadastrar(origem_id=data.origem_id, origem_tipo=data.origem_tipo, destino_id=data.destino_id, destino_tipo=data.destino_tipo, capacidade_mw=data.capacidade_mw, extensao_km=data.extensao_km)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.patch('/{id}/iniciar_construcao', response_model=LinhaTransmissaoResponse)
async def iniciar_construcao(id: UUID, data: LinhaTransmissaoDataInput, service: LinhaTransmissaoService=Depends(get_linha_transmissao_service)):
    try:
        return await service.iniciar_construcao(id, data_inicio=data.data)
    except LinhaTransmissaoNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except InvalidLinhaTransmissaoStateError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.patch('/{id}/iniciar_operacao', response_model=LinhaTransmissaoResponse)
async def iniciar_operacao(id: UUID, data: LinhaTransmissaoDataInput, service: LinhaTransmissaoService=Depends(get_linha_transmissao_service)):
    try:
        return await service.iniciar_operacao(id, data_operacao=data.data)
    except LinhaTransmissaoNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except InvalidLinhaTransmissaoStateError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.get('/', response_model=list[LinhaTransmissaoResponse])
async def listar(status_item: StatusInfraEnergia | None=None, service: LinhaTransmissaoService=Depends(get_linha_transmissao_service)):
    return await service.listar(status=status_item)
