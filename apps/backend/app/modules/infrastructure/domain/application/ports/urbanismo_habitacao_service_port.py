from __future__ import annotations
from abc import ABC, abstractmethod
from app.modules.infrastructure.domain.enums import TipoObra

class UrbanismoHabitacaoServicePort(ABC):

    @abstractmethod
    async def validar_conformidade_urbanistica(self, *, endereco: str, bairro: str, municipio: str, provincia: str, tipo_obra: TipoObra) -> bool:
        pass
