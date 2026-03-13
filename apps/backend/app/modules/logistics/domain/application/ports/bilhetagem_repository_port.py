from __future__ import annotations
from abc import ABC, abstractmethod
from datetime import datetime
from uuid import UUID
from app.modules.logistics.domain.enums import StatusReconciliacaoFinanceira
from app.modules.logistics.domain.models import BilhetagemEletronica

class BilhetagemRepositoryPort(ABC):

    @abstractmethod
    async def save(self, item: BilhetagemEletronica) -> BilhetagemEletronica:
        pass

    @abstractmethod
    async def get_by_id(self, evento_id: UUID) -> BilhetagemEletronica | None:
        pass

    @abstractmethod
    async def get_by_codigo_bilhete(self, codigo_bilhete: str) -> BilhetagemEletronica | None:
        pass

    @abstractmethod
    async def list(self, *, viagem_id: UUID | None=None, codigo_bilhete: str | None=None, status_reconciliacao: StatusReconciliacaoFinanceira | None=None, data_inicio: datetime | None=None, data_fim: datetime | None=None) -> list[BilhetagemEletronica]:
        pass
