from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import date
from uuid import UUID

from apps.backend.app.modules.resources.pescas.industrial.domain.enums import StatusInspecao
from apps.backend.app.modules.resources.pescas.industrial.domain.models.inspecao_sanitaria_industrial import (
    InspecaoSanitariaIndustrial,
)


class InspecaoSanitariaIndustrialRepositoryPort(ABC):
    @abstractmethod
    async def save(self, inspecao: InspecaoSanitariaIndustrial) -> InspecaoSanitariaIndustrial:
        pass

    @abstractmethod
    async def get_by_id(self, inspecao_id: UUID) -> InspecaoSanitariaIndustrial | None:
        pass

    @abstractmethod
    async def get_by_codigo(self, codigo_inspecao: str) -> InspecaoSanitariaIndustrial | None:
        pass

    @abstractmethod
    async def list_all(self) -> list[InspecaoSanitariaIndustrial]:
        pass

    @abstractmethod
    async def list_by_unidade(
        self, unidade_processamento_id: UUID
    ) -> list[InspecaoSanitariaIndustrial]:
        pass

    @abstractmethod
    async def list_by_status(self, status: StatusInspecao) -> list[InspecaoSanitariaIndustrial]:
        pass

    @abstractmethod
    async def list_by_lote(self, lote_producao_id: UUID) -> list[InspecaoSanitariaIndustrial]:
        pass

    @abstractmethod
    async def list_by_periodo(
        self, data_inicio: date, data_fim: date
    ) -> list[InspecaoSanitariaIndustrial]:
        pass

    @abstractmethod
    async def delete(self, inspecao_id: UUID) -> bool:
        pass

    @abstractmethod
    async def next_codigo(self) -> str:
        pass
