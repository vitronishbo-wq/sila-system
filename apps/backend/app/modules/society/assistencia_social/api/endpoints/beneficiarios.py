from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, status

from apps.backend.app.modules.society.assistencia_social.api.deps import get_beneficiario_service
from apps.backend.app.modules.society.assistencia_social.api.endpoints._errors import (
    raise_http_for_value_error,
)
from apps.backend.app.modules.society.assistencia_social.api.schemas.beneficiario_schema import (
    BeneficiarioCreate,
    BeneficiarioMotivo,
    BeneficiarioResponse,
)
from apps.backend.app.modules.society.assistencia_social.application.services.beneficiario_service import (
    BeneficiarioService,
)

router = APIRouter(prefix="/beneficiarios", tags=["Assistencia Social - Beneficiarios"])

beneficiario_service_dep = Depends(get_beneficiario_service)


@router.post("/", response_model=BeneficiarioResponse, status_code=status.HTTP_201_CREATED)
async def cadastrar_beneficiario(
    data: BeneficiarioCreate, service: BeneficiarioService = beneficiario_service_dep
) -> BeneficiarioResponse:
    try:
        return await service.cadastrar_beneficiario(
            citizen_id=data.citizen_id,
            faixa_vulnerabilidade=data.faixa_vulnerabilidade,
            cadastro_unico_id=data.cadastro_unico_id,
            observacoes=data.observacoes,
        )
    except ValueError as exc:
        raise_http_for_value_error(exc)


@router.get("/{beneficiario_id}", response_model=BeneficiarioResponse)
async def obter_beneficiario(
    beneficiario_id: UUID, service: BeneficiarioService = beneficiario_service_dep
) -> BeneficiarioResponse:
    try:
        return await service.buscar_beneficiario(beneficiario_id)
    except ValueError as exc:
        raise_http_for_value_error(exc)


@router.get("/", response_model=list[BeneficiarioResponse])
async def listar_beneficiarios(
    service: BeneficiarioService = beneficiario_service_dep,
) -> list[BeneficiarioResponse]:
    return await service.listar_beneficiarios()


@router.patch("/{beneficiario_id}/suspender", response_model=BeneficiarioResponse)
async def suspender_beneficiario(
    beneficiario_id: UUID,
    data: BeneficiarioMotivo,
    service: BeneficiarioService = beneficiario_service_dep,
) -> BeneficiarioResponse:
    try:
        return await service.suspender_beneficiario(beneficiario_id, data.motivo)
    except ValueError as exc:
        raise_http_for_value_error(exc)


@router.patch("/{beneficiario_id}/inativar", response_model=BeneficiarioResponse)
async def inativar_beneficiario(
    beneficiario_id: UUID,
    data: BeneficiarioMotivo,
    service: BeneficiarioService = beneficiario_service_dep,
) -> BeneficiarioResponse:
    try:
        return await service.inativar_beneficiario(beneficiario_id, data.motivo)
    except ValueError as exc:
        raise_http_for_value_error(exc)


@router.delete("/{beneficiario_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remover_beneficiario(
    beneficiario_id: UUID, service: BeneficiarioService = beneficiario_service_dep
) -> None:
    try:
        await service.remover_beneficiario(beneficiario_id)
    except ValueError as exc:
        raise_http_for_value_error(exc)