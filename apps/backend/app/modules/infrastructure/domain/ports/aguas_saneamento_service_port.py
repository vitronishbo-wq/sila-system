from __future__ import annotations

from abc import ABC, abstractmethod

from apps.backend.app.modules.infrastructure.domain.enums import TipoObra


class AguasSaneamentoServicePort(ABC):
    @abstractmethod
    async def validar_capacidade_rede(
        self, *, municipio: str, provincia: str, tipo_obra: TipoObra
    ) -> bool:
        pass
