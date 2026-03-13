from __future__ import annotations
from abc import ABC, abstractmethod
from uuid import UUID
from app.modules.society.desporto.domain.enums import ModalidadeDesportiva, TipoClube
from app.modules.society.desporto.domain.models.clube import Clube

class ClubeRepositoryPort(ABC):

    @abstractmethod
    async def save(self, clube: Clube) -> Clube:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, clube_id: UUID) -> Clube | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_codigo(self, codigo_clube: str) -> Clube | None:
        raise NotImplementedError

    @abstractmethod
    async def list_all(self) -> list[Clube]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_tipo(self, tipo: TipoClube) -> list[Clube]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_modalidade(self, modalidade: ModalidadeDesportiva) -> list[Clube]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_municipio(self, municipio: str) -> list[Clube]:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, clube_id: UUID) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def next_codigo(self) -> str:
        raise NotImplementedError