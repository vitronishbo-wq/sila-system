from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID

from apps.backend.app.modules.society.juventude.domain.enums import (
    Escolaridade,
    FaixaEtaria,
    SituacaoOcupacional,
)
from apps.backend.app.modules.society.juventude.domain.models.jovem import Jovem


class JovemRepositoryPort(ABC):
    @abstractmethod
    async def save(self, jovem: Jovem) -> Jovem:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, jovem_id: UUID) -> Jovem | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_registro(self, numero_registro: str) -> Jovem | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_citizen(self, citizen_id: UUID) -> Jovem | None:
        raise NotImplementedError

    @abstractmethod
    async def list_all(self) -> list[Jovem]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_faixa_etaria(self, faixa_etaria: FaixaEtaria) -> list[Jovem]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_escolaridade(self, escolaridade: Escolaridade) -> list[Jovem]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_situacao(self, situacao: SituacaoOcupacional) -> list[Jovem]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_municipio(self, municipio: str) -> list[Jovem]:
        raise NotImplementedError

    @abstractmethod
    async def list_vulneraveis(self) -> list[Jovem]:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, jovem_id: UUID) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def next_registro(self) -> str:
        raise NotImplementedError
