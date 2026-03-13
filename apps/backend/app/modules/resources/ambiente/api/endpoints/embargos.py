from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException, status
from app.modules.resources.ambiente.api.deps import get_penalidade_service
from app.modules.resources.ambiente.api.schemas.embargo_schema import EmbargoCreate, EmbargoLevantamentoInput, EmbargoResponse, EmbargoSuspensaoInput
from app.modules.resources.ambiente.application.services.penalidade_service import PenalidadeService
from app.modules.resources.ambiente.domain.enums import StatusEmbargo
from app.modules.resources.ambiente.exceptions import AutoInfracaoNotFoundError, EmbargoNotFoundError
router = APIRouter(prefix='/embargos', tags=['Ambiente - Embargos'])

@router.post('/', response_model=EmbargoResponse, status_code=status.HTTP_201_CREATED)
async def aplicar_embargo(data: EmbargoCreate, service: PenalidadeService=Depends(get_penalidade_service)):
    try:
        return await service.aplicar_embargo(numero_auto_infracao=data.numero_auto_infracao, motivo=data.motivo)
    except AutoInfracaoNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/{numero_embargo:path}/suspender', response_model=EmbargoResponse)
async def suspender_embargo(numero_embargo: str, data: EmbargoSuspensaoInput, service: PenalidadeService=Depends(get_penalidade_service)):
    try:
        return await service.suspender_embargo(numero_embargo, motivo=data.motivo)
    except EmbargoNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/{numero_embargo:path}/levantar', response_model=EmbargoResponse)
async def levantar_embargo(numero_embargo: str, data: EmbargoLevantamentoInput, service: PenalidadeService=Depends(get_penalidade_service)):
    try:
        return await service.levantar_embargo(numero_embargo, observacoes=data.observacoes)
    except EmbargoNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.get('/{numero_embargo:path}', response_model=EmbargoResponse)
async def obter_embargo(numero_embargo: str, service: PenalidadeService=Depends(get_penalidade_service)):
    try:
        return await service.obter_embargo_por_numero(numero_embargo)
    except EmbargoNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.get('/', response_model=list[EmbargoResponse])
async def listar_embargos(numero_auto_infracao: str | None=None, status_embargo: StatusEmbargo | None=None, service: PenalidadeService=Depends(get_penalidade_service)):
    return await service.listar_embargos(numero_auto_infracao=numero_auto_infracao, status=status_embargo)