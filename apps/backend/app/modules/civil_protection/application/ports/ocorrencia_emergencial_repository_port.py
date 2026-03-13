from __future__ import annotations
from abc import ABC, abstractmethod
from datetime import datetime
from uuid import UUID
from app.modules.civil_protection.domain.enums import StatusOcorrenciaEmergencial, TipoOcorrenciaEmergencial
from app.modules.civil_protection.domain.models.ocorrencia_emergencial import OcorrenciaEmergencial

class OcorrenciaEmergencialRepositoryPort(ABC):

    @abstractmethod
    async def save(self, ocorrencia: OcorrenciaEmergencial) -> OcorrenciaEmergencial:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, ocorrencia_id: UUID) -> OcorrenciaEmergencial | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_codigo(self, codigo_ocorrencia: str) -> OcorrenciaEmergencial | None:
        raise NotImplementedError

    @abstractmethod
    async def list_all(self) -> list[OcorrenciaEmergencial]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_corporacao(self, corporacao_id: UUID) -> list[OcorrenciaEmergencial]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_tipo(self, tipo: TipoOcorrenciaEmergencial) -> list[OcorrenciaEmergencial]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_status(self, status: StatusOcorrenciaEmergencial) -> list[OcorrenciaEmergencial]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_periodo(self, inicio: datetime, fim: datetime) -> list[OcorrenciaEmergencial]:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, ocorrencia_id: UUID) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def next_codigo(self) -> str:
        raise NotImplementedError