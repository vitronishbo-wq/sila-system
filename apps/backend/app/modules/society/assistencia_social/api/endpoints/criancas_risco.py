from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, status

from apps.backend.app.modules.society.assistencia_social.api.deps import get_crianca_risco_service
from apps.backend.app.modules.society.assistencia_social.api.endpoints._errors import (
    raise_http_for_value_error,
)
from apps.backend.app.modules.society.assistencia_social.api.schemas.crianca_risco_schema import (
    CriancaRiscoCreate,
    CriancaRiscoResponse,
)
from apps.backend.app.modules.society.assistencia_social.application.services.crianca_risco_service import (
    CriancaRiscoService,
)

router = APIRouter(prefix="/criancas-risco", tags=["Assistencia Social - Criancas Risco"])

crianca_risco_service_dep = Depends(get_crianca_risco_service)


@router.post("/", response_model=CriancaRiscoResponse, status_code=status.HTTP_201_CREATED)
async def registrar_crianca_risco(
    data: CriancaRiscoCreate, service: CriancaRiscoService = crianca_risco_service_dep
) -> CriancaRiscoResponse:
    try:
        return await service.registrar_crianca_risco(
            beneficiario_id=data.beneficiario_id,
            citizen_id_crianca=data.citizen_id_crianca,
            idade=data.idade,
            motivo=data.motivo,
            escolarizada=data.escolarizada,
        )
    except ValueError as exc:
        raise_http_for_value_error(exc)


@router.get("/{item_id}", response_model=CriancaRiscoResponse)
async def obter_crianca_risco(
    item_id: UUID, service: CriancaRiscoService = crianca_risco_service_dep
) -> CriancaRiscoResponse:
    try:
        return await service.buscar_crianca_risco(item_id)
    except ValueError as exc:
        raise_http_for_value_error(exc)


@router.get("/", response_model=list[CriancaRiscoResponse])
async def listar_criancas_risco(
    beneficiario_id: UUID | None = None,
    service: CriancaRiscoService = crianca_risco_service_dep,
) -> list[CriancaRiscoResponse]:
    return await service.listar_criancas_risco(beneficiario_id=beneficiario_id)


@router.patch("/{item_id}/encerrar", response_model=CriancaRiscoResponse)
async def encerrar_crianca_risco(
    item_id: UUID, service: CriancaRiscoService = crianca_risco_service_dep
) -> CriancaRiscoResponse:
    try:
        return await service.encerrar_crianca_risco(item_id)
    except ValueError as exc:
        raise_http_for_value_error(exc)


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remover_crianca_risco(
    item_id: UUID, service: CriancaRiscoService = crianca_risco_service_dep
) -> None:
    try:
        await service.remover_crianca_risco(item_id)
    except ValueError as exc:
        raise_http_for_value_error(exc)