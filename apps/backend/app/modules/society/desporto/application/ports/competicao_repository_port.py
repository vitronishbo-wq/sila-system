from __future__ import annotations
from abc import ABC, abstractmethod
from datetime import date
from uuid import UUID
from app.modules.society.desporto.domain.enums import ModalidadeDesportiva, StatusCompeticao, TipoCompeticao
from app.modules.society.desporto.domain.models.competicao import Competicao

class CompeticaoRepositoryPort(ABC):

    @abstractmethod
    async def save(self, competicao: Competicao) -> Competicao:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, competicao_id: UUID) -> Competicao | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_codigo(self, codigo_competicao: str) -> Competicao | None:
        raise NotImplementedError

    @abstractmethod
    async def list_all(self) -> list[Competicao]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_tipo(self, tipo: TipoCompeticao) -> list[Competicao]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_modalidade(self, modalidade: ModalidadeDesportiva) -> list[Competicao]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_status(self, status: StatusCompeticao) -> list[Competicao]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_periodo(self, data_inicio: date, data_fim: date) -> list[Competicao]:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, competicao_id: UUID) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def next_codigo(self) -> str:
        raise NotImplementedError