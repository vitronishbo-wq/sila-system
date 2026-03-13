from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import date
from typing import Any
from uuid import UUID


class JuventudeServicePort(ABC):

    @abstractmethod
    async def get_jovem_profile(self, citizen_id: UUID) -> dict | None:
        pass

    @abstractmethod
    async def atualizar_carteira_vacinacao(
        self, *, citizen_id: UUID, vacinas: list[dict[str, Any]]
    ) -> None:
        pass

    @abstractmethod
    async def registrar_meta_saude_alcancada(
        self, *, citizen_id: UUID, meta: str, data_referencia: date
    ) -> None:
        pass
