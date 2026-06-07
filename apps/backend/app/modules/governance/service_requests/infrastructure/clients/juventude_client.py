from __future__ import annotations

from typing import Any
from uuid import UUID

from apps.backend.app.modules.governance.service_requests.application.ports import (
    JuventudeClientPort,
)
from apps.backend.app.modules.governance.service_requests.domain.enums import ServiceType
from apps.backend.app.modules.governance.service_requests.infrastructure.clients._helpers import (
    parse_uuid,
)


class JuventudeClient(JuventudeClientPort):
    """Client para validação de inscrições em serviços de Juventude."""

    def __init__(self, jovem_repo: Any, programa_repo: Any) -> None:
        self._jovem_repo = jovem_repo
        self._programa_repo = programa_repo

    async def validate_payload(
        self, *, service_type: str, citizen_id: UUID, payload: dict[str, Any]
    ) -> tuple[bool, str | None]:
        if service_type != ServiceType.YOUTH_PROGRAM.value:
            return (True, None)
        jovem = await self._jovem_repo.get_by_citizen(citizen_id)
        if jovem is None:
            return (False, "Jovem não cadastrado no módulo de Juventude")
        programa_id, err = parse_uuid(payload.get("programa_id"), "programa_id")
        if err:
            return (False, err)
        programa = await self._programa_repo.get_by_id(programa_id)
        if programa is None:
            return (False, "Programa de juventude não encontrado")
        status = str(getattr(programa.status, "value", programa.status)).lower()
        if status not in {"inscricoes_abertas", "ativo"}:
            return (False, "Programa não está apto para novas inscrições")
        return (True, None)

    async def submit(
        self, *, service_type: str, request_id: UUID, citizen_id: UUID, payload: dict[str, Any]
    ) -> dict[str, Any]:
        return {
            "module": "juventude",
            "service_type": service_type,
            "request_id": str(request_id),
            "citizen_id": str(citizen_id),
            "programa_id": str(payload.get("programa_id")) if payload.get("programa_id") else None,
            "accepted": True,
        }
