from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from apps.backend.app.modules.society.seguranca_social.api.deps import get_beneficiario_service
from apps.backend.app.modules.society.seguranca_social.api.schemas.beneficiario_schema import (
    BeneficiarioCreate,
    BeneficiarioFilter,
    BeneficiarioResponse,
)
from apps.backend.app.modules.society.seguranca_social.application.services import (
    BeneficiarioService,
)
from apps.backend.app.modules.society.seguranca_social.exceptions import (
    BeneficiarioAlreadyExistsError,
    BeneficiarioNotFoundError,
    CandidatoEmpregoRequiredError,
    CitizenNotFoundError,
)

router = APIRouter(prefix="/beneficiarios", tags=["Seguranca Social - Beneficiarios"])

beneficiario_service_dep = Depends(get_beneficiario_service)
filtros_dep = Depends()


@router.post("/", response_model=BeneficiarioResponse, status_code=status.HTTP_201_CREATED)
async def inscrever_beneficiario(
    data: BeneficiarioCreate, service: BeneficiarioService = beneficiario_service_dep
):
    try:
        return await service.inscrever_beneficiario(
            citizen_id=data.citizen_id, tipo=data.tipo, regime=data.regime
        )
    except CitizenNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except BeneficiarioAlreadyExistsError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    except CandidatoEmpregoRequiredError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/{beneficiario_id}/ativar", response_model=BeneficiarioResponse)
async def ativar_beneficiario(
    beneficiario_id: UUID, service: BeneficiarioService = beneficiario_service_dep
):
    try:
        return await service.ativar_beneficiario(beneficiario_id=beneficiario_id)
    except BeneficiarioNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get("/{beneficiario_id}", response_model=BeneficiarioResponse)
async def obter_beneficiario(
    beneficiario_id: UUID, service: BeneficiarioService = beneficiario_service_dep
):
    beneficiario = await service.obter_por_id(beneficiario_id)
    if not beneficiario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Beneficiario nao encontrado"
        )
    return beneficiario


@router.get("/", response_model=list[BeneficiarioResponse])
async def listar_beneficiarios(
    filtros: BeneficiarioFilter = filtros_dep,
    service: BeneficiarioService = beneficiario_service_dep,
):
    return await service.listar_beneficiarios(
        tipo=filtros.tipo, estado=filtros.estado, regime=filtros.regime
    )