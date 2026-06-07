from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any


class ReclamacaoRepositoryPort(ABC):
    @abstractmethod
    async def create(self, data: dict[str, Any]) -> dict[str, Any]:
        pass

    @abstractmethod
    async def get_by_id(self, reclamacao_id: int) -> dict[str, Any] | None:
        pass

    @abstractmethod
    async def get_by_protocolo(self, protocolo: str) -> dict[str, Any] | None:
        pass

    @abstractmethod
    async def list_by_consumidor(
        self, consumidor_id: int, limit: int = 50, offset: int = 0
    ) -> list[dict[str, Any]]:
        pass

    @abstractmethod
    async def list_by_estabelecimento(
        self, estabelecimento_id: int, limit: int = 50, offset: int = 0
    ) -> list[dict[str, Any]]:
        pass

    @abstractmethod
    async def list_by_status(
        self, status: str, limit: int = 100, offset: int = 0
    ) -> list[dict[str, Any]]:
        pass

    @abstractmethod
    async def list_by_periodo(
        self, data_inicio: datetime, data_fim: datetime
    ) -> list[dict[str, Any]]:
        pass

    @abstractmethod
    async def list_prioritarias(self, prioridade: str, limit: int = 50) -> list[dict[str, Any]]:
        pass

    @abstractmethod
    async def update(self, data: dict[str, Any]) -> dict[str, Any]:
        pass

    @abstractmethod
    async def delete(self, reclamacao_id: int) -> bool:
        pass

    @abstractmethod
    async def count_by_status(self, status: str) -> int:
        pass

    @abstractmethod
    async def count_total(self) -> int:
        pass
