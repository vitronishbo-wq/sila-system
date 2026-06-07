from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from apps.backend.app.modules.society.seguranca_social.api.deps import get_pensao_service
from apps.backend.app.modules.society.seguranca_social.api.schemas.pensao_schema import (
    PensaoAction,
    PensaoCreate,
    PensaoFilter,
    PensaoMotivo,
    PensaoResponse,
)
from apps.backend.app.modules.society.seguranca_social.application.services import PensaoService
from apps.backend.app.modules.society.seguranca_social.exceptions import (
    BeneficiarioNotEligibleError,
    BeneficiarioNotFoundError,
    PensaoAlreadyExistsError,
    PensaoNotFoundError,
)

router = APIRouter(prefix="/pensoes", tags=["Seguranca Social - Pensoes"])

pensao_service_dep = Depends(get_pensao_service)
filtros_dep = Depends()


@router.post("/", response_model=PensaoResponse, status_code=status.HTTP_201_CREATED)
async def solicitar_pensao(
    data: PensaoCreate, service: PensaoService = pensao_service_dep
):
    try:
        return await service.solicitar_pensao(
            beneficiario_id=data.beneficiario_id,
            tipo=data.tipo,
            valor_mensal=data.valor_mensal,
            conta_bancaria=data.conta_bancaria,
            iban=data.iban,
        )
    except BeneficiarioNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except BeneficiarioNotEligibleError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    except PensaoAlreadyExistsError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/{pensao_id}/aprovar", response_model=PensaoResponse)
async def aprovar_pensao(
    pensao_id: UUID, data: PensaoAction, service: PensaoService = pensao_service_dep
):
    try:
        return await service.aprovar_pensao(pensao_id=pensao_id, actor_id=data.actor_id)
    except PensaoNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/{pensao_id}/suspender", response_model=PensaoResponse)
async def suspender_pensao(
    pensao_id: UUID, data: PensaoMotivo, service: PensaoService = pensao_service_dep
):
    try:
        return await service.suspender_pensao(pensao_id=pensao_id, motivo=data.motivo)
    except PensaoNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/{pensao_id}/cancelar", response_model=PensaoResponse)
async def cancelar_pensao(
    pensao_id: UUID, data: PensaoMotivo, service: PensaoService = pensao_service_dep
):
    try:
        return await service.cancelar_pensao(pensao_id=pensao_id, motivo=data.motivo)
    except PensaoNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get("/{pensao_id}", response_model=PensaoResponse)
async def obter_pensao(pensao_id: UUID, service: PensaoService = pensao_service_dep):
    pensao = await service.obter_por_id(pensao_id)
    if not pensao:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pensao nao encontrada")
    return pensao


@router.get("/", response_model=list[PensaoResponse])
async def listar_pensoes(
    filtros: PensaoFilter = filtros_dep, service: PensaoService = pensao_service_dep
):
    return await service.listar_pensoes(
        beneficiario_id=filtros.beneficiario_id, tipo=filtros.tipo, status=filtros.status
    )