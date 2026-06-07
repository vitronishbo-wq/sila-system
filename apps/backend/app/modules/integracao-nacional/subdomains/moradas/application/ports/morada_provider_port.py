from abc import ABC, abstractmethod

from ...domain.models import (
    Morada,
    MoradaNormalizada,
    MoradaValidationResult,
)


class MoradaProviderPort(ABC):
    @abstractmethod
    async def geocodificar(self, morada: Morada) -> MoradaNormalizada:
        pass

    @abstractmethod
    async def validar(self, morada: Morada) -> MoradaValidationResult:
        pass

    @abstractmethod
    async def obter_provincias(self) -> list[str]:
        pass

    @abstractmethod
    async def obter_municipios(self, provincia: str) -> list[str]:
        pass
