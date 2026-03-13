from __future__ import annotations
from app.modules.economy.trade.external.application.ports import SuspensaoRadarRepositoryPort
from app.modules.economy.trade.external.domain.models import SuspensaoRadar
from app.modules.economy.trade.external.infrastructure.repositories.in_memory_habilitacao_repository_base import InMemoryHabilitacaoRepositoryBase

class InMemorySuspensaoRadarRepository(InMemoryHabilitacaoRepositoryBase[SuspensaoRadar], SuspensaoRadarRepositoryPort):
    pass