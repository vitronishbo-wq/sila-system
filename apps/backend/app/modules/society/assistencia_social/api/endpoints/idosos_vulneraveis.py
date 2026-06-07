from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, status

from apps.backend.app.modules.society.assistencia_social.api.deps import (
    get_idoso_vulneravel_service,
)
from apps.backend.app.modules.society.assistencia_social.api.endpoints._errors import (
    raise_http_for_value_error,
)
from apps.backend.app.modules.society.assistencia_social.api.schemas.idoso_vulneravel_schema import (
    IdosoVulneravelCreate,
    IdosoVulneravelResponse,
)
from apps.backend.app.modules.society.assistencia_social.application.services.idoso_vulneravel_service import (
    IdosoVulneravelService,
)

router = APIRouter(prefix="/idosos-vulneraveis", tags=["Assistencia Social - Idosos Vulneraveis"])

idoso_vulneravel_service_dep = Depends(get_idoso_vulneravel_service)


@router.post("/", response_model=IdosoVulneravelResponse, status_code=status.HTTP_201_CREATED)
async def registrar_idoso_vulneravel(
    data: IdosoVulneravelCreate,
    service: IdosoVulneravelService = idoso_vulneravel_service_dep,
) -> IdosoVulneravelResponse:
    try:
        return await service.registrar_idoso(
            beneficiario_id=data.beneficiario_id,
            citizen_id_idoso=data.citizen_id_idoso,
            idade=data.idade,
            dependencia=data.dependencia,
            precisa_cuidados=data.precisa_cuidados,
        )
    except ValueError as exc:
        raise_http_for_value_error(exc)


@router.get("/{item_id}", response_model=IdosoVulneravelResponse)
async def obter_idoso_vulneravel(
    item_id: UUID, service: IdosoVulneravelService = idoso_vulneravel_service_dep
) -> IdosoVulneravelResponse:
    try:
        return await service.buscar_idoso(item_id)
    except ValueError as exc:
        raise_http_for_value_error(exc)


@router.get("/", response_model=list[IdosoVulneravelResponse])
async def listar_idosos_vulneraveis(
    beneficiario_id: UUID | None = None,
    service: IdosoVulneravelService = idoso_vulneravel_service_dep,
) -> list[IdosoVulneravelResponse]:
    return await service.listar_idosos(beneficiario_id=beneficiario_id)


@router.patch("/{item_id}/encerrar", response_model=IdosoVulneravelResponse)
async def encerrar_idoso_vulneravel(
    item_id: UUID, service: IdosoVulneravelService = idoso_vulneravel_service_dep
) -> IdosoVulneravelResponse:
    try:
        return await service.encerrar_idoso(item_id)
    except ValueError as exc:
        raise_http_for_value_error(exc)


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remover_idoso_vulneravel(
    item_id: UUID, service: IdosoVulneravelService = idoso_vulneravel_service_dep
) -> None:
    try:
        await service.remover_idoso(item_id)
    except ValueError as exc:
        raise_http_for_value_error(exc)