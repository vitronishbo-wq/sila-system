from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID

from apps.backend.app.modules.society.juventude.domain.enums import StatusFormacao
from apps.backend.app.modules.society.juventude.domain.models.formacao_juvenil import (
    FormacaoJuvenil,
)


class FormacaoRepositoryPort(ABC):
    @abstractmethod
    async def save(self, formacao: FormacaoJuvenil) -> FormacaoJuvenil:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, formacao_id: UUID) -> FormacaoJuvenil | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_codigo(self, codigo_formacao: str) -> FormacaoJuvenil | None:
        raise NotImplementedError

    @abstractmethod
    async def list_all(self) -> list[FormacaoJuvenil]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_jovem(self, jovem_id: UUID) -> list[FormacaoJuvenil]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_programa(self, programa_id: UUID) -> list[FormacaoJuvenil]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_status(self, status: StatusFormacao) -> list[FormacaoJuvenil]:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, formacao_id: UUID) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def next_codigo(self) -> str:
        raise NotImplementedError
