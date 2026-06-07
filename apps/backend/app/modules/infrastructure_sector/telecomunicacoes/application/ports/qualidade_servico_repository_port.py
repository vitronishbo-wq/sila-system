from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID

from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.domain.enums import (
    StatusQualidadeServico,
)
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.domain.models.qualidade_servico import (
    QualidadeServico,
)


class QualidadeServicoRepositoryPort(ABC):
    @abstractmethod
    async def save(self, medicao: QualidadeServico) -> QualidadeServico:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, medicao_id: UUID) -> QualidadeServico | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_codigo(self, codigo_medicao: str) -> QualidadeServico | None:
        raise NotImplementedError

    @abstractmethod
    async def list_all(self) -> list[QualidadeServico]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_operadora(self, operadora_id: UUID) -> list[QualidadeServico]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_operadora_periodo(
        self, operadora_id: UUID, referencia_ano: int, referencia_mes: int
    ) -> list[QualidadeServico]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_assinante(self, assinante_id: UUID) -> list[QualidadeServico]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_status(self, status: StatusQualidadeServico) -> list[QualidadeServico]:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, medicao_id: UUID) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def next_codigo(self) -> str:
        raise NotImplementedError
