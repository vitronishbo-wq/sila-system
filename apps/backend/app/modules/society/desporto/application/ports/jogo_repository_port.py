from __future__ import annotations
from abc import ABC, abstractmethod
from datetime import date
from uuid import UUID
from app.modules.society.desporto.domain.enums import StatusJogo
from app.modules.society.desporto.domain.models.jogo import Jogo

class JogoRepositoryPort(ABC):

    @abstractmethod
    async def save(self, jogo: Jogo) -> Jogo:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, jogo_id: UUID) -> Jogo | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_codigo(self, codigo_jogo: str) -> Jogo | None:
        raise NotImplementedError

    @abstractmethod
    async def list_all(self) -> list[Jogo]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_competicao(self, competicao_id: UUID) -> list[Jogo]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_clube(self, clube_id: UUID) -> list[Jogo]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_status(self, status: StatusJogo) -> list[Jogo]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_periodo(self, data_inicio: date, data_fim: date) -> list[Jogo]:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, jogo_id: UUID) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def next_codigo(self) -> str:
        raise NotImplementedError