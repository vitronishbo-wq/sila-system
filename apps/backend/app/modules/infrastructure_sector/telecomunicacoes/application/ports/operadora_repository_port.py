from __future__ import annotations
from abc import ABC, abstractmethod
from uuid import UUID
from app.modules.infrastructure_sector.telecomunicacoes.domain.enums import TipoServico
from app.modules.infrastructure_sector.telecomunicacoes.domain.models.operadora import Operadora

class OperadoraRepositoryPort(ABC):

    @abstractmethod
    async def save(self, operadora: Operadora) -> Operadora:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, operadora_id: UUID) -> Operadora | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_cnpj(self, cnpj: str) -> Operadora | None:
        raise NotImplementedError

    @abstractmethod
    async def list_all(self) -> list[Operadora]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_servico(self, servico: TipoServico) -> list[Operadora]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_municipio(self, municipio: str) -> list[Operadora]:
        raise NotImplementedError

    @abstractmethod
    async def list_ativas(self) -> list[Operadora]:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, operadora_id: UUID) -> bool:
        raise NotImplementedError