from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any
from uuid import UUID


class RequestServicePort(ABC):
    @abstractmethod
    async def create_request(
        self,
        *,
        request_type: str,
        entity_id: UUID,
        citizen_id: UUID,
        numero_processo: str,
        metadata: dict[str, Any] | None = None,
    ) -> UUID:
        pass

    @abstractmethod
    async def complete_request(
        self, *, entity_id: UUID, actor_id: UUID, metadata: dict[str, Any] | None = None
    ) -> bool:
        pass
