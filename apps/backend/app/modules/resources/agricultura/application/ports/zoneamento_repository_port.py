from __future__ import annotations
from abc import ABC, abstractmethod
from apps.backend.app.modules.resources.agricultura.domain.enums import StatusCadastroAmbiental, StatusZoneamento
from apps.backend.app.modules.resources.agricultura.domain.models.cadastro_ambiental import CadastroAmbiental
from apps.backend.app.modules.resources.agricultura.domain.models.zoneamento import Zoneamento

class ZoneamentoRepositoryPort(ABC):

    @abstractmethod
    async def save_zoneamento(self, item: Zoneamento) -> Zoneamento:
        pass

    @abstractmethod
    async def get_zoneamento_by_codigo(self, codigo_zoneamento: str) -> Zoneamento | None:
        pass

    @abstractmethod
    async def list_zoneamentos(self, *, codigo_propriedade: str | None=None, status: StatusZoneamento | None=None) -> list[Zoneamento]:
        pass

    @abstractmethod
    async def next_codigo_zoneamento(self) -> str:
        pass

    @abstractmethod
    async def save_cadastro_ambiental(self, item: CadastroAmbiental) -> CadastroAmbiental:
        pass

    @abstractmethod
    async def get_cadastro_ambiental_by_codigo(self, codigo_cadastro_ambiental: str) -> CadastroAmbiental | None:
        pass

    @abstractmethod
    async def get_cadastro_ambiental_by_zoneamento(self, codigo_zoneamento: str) -> CadastroAmbiental | None:
        pass

    @abstractmethod
    async def list_cadastros_ambientais(self, *, codigo_propriedade: str | None=None, status: StatusCadastroAmbiental | None=None) -> list[CadastroAmbiental]:
        pass

    @abstractmethod
    async def next_codigo_cadastro_ambiental(self) -> str:
        pass