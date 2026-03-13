from __future__ import annotations
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from apps.backend.app.modules.energy.api.deps import get_central_geradora_service
from apps.backend.app.modules.energy.api.schemas.central_geradora_schema import CentralGeradoraCreate, CentralGeradoraDataInput, CentralGeradoraResponse
from apps.backend.app.modules.energy.application.services import CentralGeradoraService
from apps.backend.app.modules.energy.domain.enums import FonteEnergia, StatusInfraEnergia
from apps.backend.app.modules.energy.core.exceptions import CentralGeradoraNotFoundError, InvalidCentralGeradoraStateError
router = APIRouter(prefix='/central_geradora', tags=['Energia - Central Geradora'])

@router.post('/', response_model=CentralGeradoraResponse, status_code=status.HTTP_201_CREATED)
async def cadastrar(data: CentralGeradoraCreate, service: CentralGeradoraService=Depends(get_central_geradora_service)):
    try:
        return await service.cadastrar(nome=data.nome, tipo=data.tipo, capacidade_instalada_mw=data.capacidade_instalada_mw, municipio=data.municipio, provincia=data.provincia)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.patch('/{id}/iniciar_construcao', response_model=CentralGeradoraResponse)
async def iniciar_construcao(id: UUID, data: CentralGeradoraDataInput, service: CentralGeradoraService=Depends(get_central_geradora_service)):
    try:
        return await service.iniciar_construcao(id, data_inicio=data.data)
    except CentralGeradoraNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except InvalidCentralGeradoraStateError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.patch('/{id}/iniciar_operacao', response_model=CentralGeradoraResponse)
async def iniciar_operacao(id: UUID, data: CentralGeradoraDataInput, service: CentralGeradoraService=Depends(get_central_geradora_service)):
    try:
        return await service.iniciar_operacao(id, data_operacao=data.data)
    except CentralGeradoraNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except InvalidCentralGeradoraStateError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.get('/', response_model=list[CentralGeradoraResponse])
async def listar(status_item: StatusInfraEnergia | None=None, tipo: FonteEnergia | None=None, service: CentralGeradoraService=Depends(get_central_geradora_service)):
    return await service.listar(status=status_item, tipo=tipo)
