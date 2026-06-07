from __future__ import annotations

from datetime import date
from typing import Any
from uuid import UUID

from apps.backend.app.modules.society.familia.application.ports.citizen_service_port import (
    CitizenServicePort,
)


class CitizenServiceAdapter(CitizenServicePort):
    """Anti-corruption layer para identidade_civil (via repositorio canonico)."""

    def __init__(self, citizen_repository) -> None:
        self._citizen_repository = citizen_repository

    async def get_citizen(self, citizen_id: UUID) -> dict[str, Any]:
        citizen = await self._citizen_repository.get_by_id(citizen_id)
        if citizen is None:
            raise ValueError(f"Cidadao {citizen_id} nao encontrado em identidade_civil")
        if hasattr(citizen, "to_dict"):
            return citizen.to_dict()
        return {
            "citizen_id": str(citizen_id),
            "birth_date": getattr(citizen, "birth_date", None),
            "vital_status": getattr(citizen, "vital_status", None),
            "is_active": getattr(citizen, "is_active", True),
        }

    async def verify_civil_capacity(self, citizen_id: UUID) -> bool:
        citizen = await self.get_citizen(citizen_id)
        status_ok = str(citizen.get("vital_status") or "alive").lower() in {"alive", "active"}
        active_ok = bool(citizen.get("is_active", True))
        age_ok = await self.get_age(citizen_id) >= 18
        return bool(status_ok and active_ok and age_ok)

    async def get_age(self, citizen_id: UUID) -> int:
        citizen = await self.get_citizen(citizen_id)
        birth_date_raw = citizen.get("birth_date")
        if birth_date_raw is None:
            return 0
        if isinstance(birth_date_raw, date):
            birth_date = birth_date_raw
        else:
            birth_date = date.fromisoformat(str(birth_date_raw))
        today = date.today()
        return (
            today.year
            - birth_date.year
            - ((today.month, today.day) < (birth_date.month, birth_date.day))
        )
