from __future__ import annotations

from abc import ABC, abstractmethod


class ServiceRequestsServicePort(ABC):
    @abstractmethod
    async def abrir_solicitacao(self, payload: dict) -> str:
        pass
