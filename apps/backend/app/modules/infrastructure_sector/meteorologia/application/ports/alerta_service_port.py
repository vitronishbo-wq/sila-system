from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any
from uuid import UUID

class AlertaServicePort(ABC):

    @abstractmethod
    async def publicar_alerta(self, *, estacao_id: UUID, alerta: dict[str, Any], observacao_id: UUID | None=None) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def notificar_defesa_civil(self, *, alertas: list[dict[str, Any]], provincia: str) -> bool:
        raise NotImplementedError