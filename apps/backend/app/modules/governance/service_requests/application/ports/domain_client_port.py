from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any
from uuid import UUID


class DomainClientPort(ABC):
    """Contrato base para clients de integração por domínio."""

    @abstractmethod
    async def validate_payload(
        self, *, service_type: str, citizen_id: UUID, payload: dict[str, Any]
    ) -> tuple[bool, str | None]:
        """
        Valida payload para criação/submissão de pedido.

        Retorna:
            tuple[bool, str | None]: (válido, mensagem_erro)
        """

    @abstractmethod
    async def submit(
        self, *, service_type: str, request_id: UUID, citizen_id: UUID, payload: dict[str, Any]
    ) -> dict[str, Any]:
        """Executa integração no domínio e retorna dados de roteamento/resultado."""
