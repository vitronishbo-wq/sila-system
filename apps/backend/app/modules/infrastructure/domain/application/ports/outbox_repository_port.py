from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any
from uuid import UUID

class OutboxRepositoryPort(ABC):

    @abstractmethod
    async def save(self, *, tenant_id: str, aggregate_type: str, aggregate_id: str, event: Any, correlation_id: str) -> UUID:
        pass