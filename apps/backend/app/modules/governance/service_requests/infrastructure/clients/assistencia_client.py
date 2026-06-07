from __future__ import annotations

from typing import Any
from uuid import UUID

from apps.backend.app.modules.governance.service_requests.application.ports import (
    AssistenciaClientPort,
)
from apps.backend.app.modules.governance.service_requests.domain.enums import ServiceType
from apps.backend.app.modules.governance.service_requests.infrastructure.clients._helpers import (
    parse_uuid,
)


class AssistenciaClient(AssistenciaClientPort):
    """Client para validação de solicitações de Assistência Social."""

    def __init__(self, beneficiario_repo: Any) -> None:
        self._beneficiario_repo = beneficiario_repo

    async def validate_payload(
        self, *, service_type: str, citizen_id: UUID, payload: dict[str, Any]
    ) -> tuple[bool, str | None]:
        if service_type != ServiceType.SOCIAL_BENEFIT.value:
            return (True, None)
        cadastro_unico_id = payload.get("cadastro_unico_id")
        if cadastro_unico_id:
            _, err = parse_uuid(cadastro_unico_id, "cadastro_unico_id")
            if err:
                return (False, err)
        beneficiario = await self._beneficiario_repo.get_by_citizen(citizen_id)
        if beneficiario is None and (not cadastro_unico_id):
            return (False, "Beneficiário não encontrado e cadastro_unico_id não informado")
        return (True, None)

    async def submit(
        self, *, service_type: str, request_id: UUID, citizen_id: UUID, payload: dict[str, Any]
    ) -> dict[str, Any]:
        beneficiario = await self._beneficiario_repo.get_by_citizen(citizen_id)
        return {
            "module": "assistencia_social",
            "service_type": service_type,
            "request_id": str(request_id),
            "citizen_id": str(citizen_id),
            "beneficiario_id": str(beneficiario.id) if beneficiario else None,
            "cadastro_unico_id": str(payload.get("cadastro_unico_id"))
            if payload.get("cadastro_unico_id")
            else None,
            "accepted": True,
        }
