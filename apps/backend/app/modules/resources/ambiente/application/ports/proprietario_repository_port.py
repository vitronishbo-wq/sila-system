from __future__ import annotations
from abc import ABC, abstractmethod
from uuid import UUID
from app.modules.resources.ambiente.domain.models.proprietario import Proprietario

class ProprietarioRepositoryPort(ABC):

    @abstractmethod
    async def save(self, item: Proprietario) -> Proprietario:
        pass

    @abstractmethod
    async def get_by_id(self, proprietario_id: UUID) -> Proprietario | None:
        pass

    @abstractmethod
    async def get_by_documento(self, documento: str) -> Proprietario | None:
        pass

    @abstractmethod
    async def next_codigo(self) -> str:
        pass