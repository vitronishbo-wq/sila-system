from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any
from uuid import UUID

class ServiceRequestsServicePort(ABC):

    @abstractmethod
    async def get_request(self, request_id: UUID) -> Any | None:
        pass

    @abstractmethod
    async def get_valor_taxa(self, request_id: UUID) -> float:
        pass

    @abstractmethod
    async def registrar_pagamento_taxa(self, request_id: UUID, pagamento_id: str, valor: float) -> None:
        pass