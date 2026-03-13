from __future__ import annotations
from abc import ABC, abstractmethod
from datetime import datetime
from uuid import UUID
from apps.backend.app.modules.public_security.domain.enums import StatusOcorrencia, TipoOcorrencia
from apps.backend.app.modules.public_security.domain.models.ocorrencia import Ocorrencia

class OcorrenciaRepositoryPort(ABC):

    @abstractmethod
    async def save(self, ocorrencia: Ocorrencia) -> Ocorrencia:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, ocorrencia_id: UUID) -> Ocorrencia | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_codigo(self, codigo_ocorrencia: str) -> Ocorrencia | None:
        raise NotImplementedError

    @abstractmethod
    async def list_all(self) -> list[Ocorrencia]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_unidade(self, unidade_id: UUID) -> list[Ocorrencia]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_tipo(self, tipo: TipoOcorrencia) -> list[Ocorrencia]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_status(self, status: StatusOcorrencia) -> list[Ocorrencia]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_periodo(self, inicio: datetime, fim: datetime) -> list[Ocorrencia]:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, ocorrencia_id: UUID) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def next_codigo(self) -> str:
        raise NotImplementedError