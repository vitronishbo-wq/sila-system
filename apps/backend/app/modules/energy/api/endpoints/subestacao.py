from __future__ import annotations
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from apps.backend.app.modules.energy.api.deps import get_subestacao_service
from apps.backend.app.modules.energy.api.schemas.subestacao_schema import SubestacaoCreate, SubestacaoDataInput, SubestacaoResponse
from apps.backend.app.modules.energy.application.services import SubestacaoService
from apps.backend.app.modules.energy.domain.enums import StatusInfraEnergia
from apps.backend.app.modules.energy.core.exceptions import InvalidSubestacaoStateError, SubestacaoNotFoundError
router = APIRouter(prefix='/subestacao', tags=['Energia - Subestacao'])

@router.post('/', response_model=SubestacaoResponse, status_code=status.HTTP_201_CREATED)
async def cadastrar(data: SubestacaoCreate, service: SubestacaoService=Depends(get_subestacao_service)):
    try:
        return await service.cadastrar(nome=data.nome, tensao_nominal_kv=data.tensao_nominal_kv, classe_tensao=data.classe_tensao, municipio=data.municipio, provincia=data.provincia)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.patch('/{id}/iniciar_construcao', response_model=SubestacaoResponse)
async def iniciar_construcao(id: UUID, data: SubestacaoDataInput, service: SubestacaoService=Depends(get_subestacao_service)):
    try:
        return await service.iniciar_construcao(id, data_inicio=data.data)
    except SubestacaoNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except InvalidSubestacaoStateError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.patch('/{id}/iniciar_operacao', response_model=SubestacaoResponse)
async def iniciar_operacao(id: UUID, data: SubestacaoDataInput, service: SubestacaoService=Depends(get_subestacao_service)):
    try:
        return await service.iniciar_operacao(id, data_operacao=data.data)
    except SubestacaoNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except InvalidSubestacaoStateError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.get('/', response_model=list[SubestacaoResponse])
async def listar(status_item: StatusInfraEnergia | None=None, service: SubestacaoService=Depends(get_subestacao_service)):
    return await service.listar(status=status_item)
