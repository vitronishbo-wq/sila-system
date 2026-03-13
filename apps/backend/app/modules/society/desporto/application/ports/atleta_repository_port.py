from __future__ import annotations
from abc import ABC, abstractmethod
from uuid import UUID
from apps.backend.app.modules.society.desporto.domain.enums import ModalidadeDesportiva, StatusAtleta, TipoAtleta
from apps.backend.app.modules.society.desporto.domain.models.atleta import Atleta

class AtletaRepositoryPort(ABC):

    @abstractmethod
    async def save(self, atleta: Atleta) -> Atleta:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, atleta_id: UUID) -> Atleta | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_registro(self, numero_registro: str) -> Atleta | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_citizen(self, citizen_id: UUID) -> Atleta | None:
        raise NotImplementedError

    @abstractmethod
    async def list_all(self) -> list[Atleta]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_clube(self, clube_id: UUID) -> list[Atleta]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_modalidade(self, modalidade: ModalidadeDesportiva) -> list[Atleta]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_status(self, status: StatusAtleta) -> list[Atleta]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_tipo(self, tipo: TipoAtleta) -> list[Atleta]:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, atleta_id: UUID) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def next_registro(self) -> str:
        raise NotImplementedError