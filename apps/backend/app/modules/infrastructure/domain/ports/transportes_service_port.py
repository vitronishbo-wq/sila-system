from __future__ import annotations
from abc import ABC, abstractmethod
from apps.backend.app.modules.infrastructure.domain.enums import TipoObra

class TransportesServicePort(ABC):

    @abstractmethod
    async def validar_impacto_viario(self, *, municipio: str, provincia: str, tipo_obra: TipoObra) -> bool:
        pass