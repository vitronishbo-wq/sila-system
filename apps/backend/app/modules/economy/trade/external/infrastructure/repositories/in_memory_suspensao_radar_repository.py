from __future__ import annotations

from apps.backend.app.modules.economy.trade.external.application.ports import (
    SuspensaoRadarRepositoryPort,
)
from apps.backend.app.modules.economy.trade.external.domain.models import SuspensaoRadar
from apps.backend.app.modules.economy.trade.external.infrastructure.repositories.in_memory_habilitacao_repository_base import (
    InMemoryHabilitacaoRepositoryBase,
)


class InMemorySuspensaoRadarRepository(
    InMemoryHabilitacaoRepositoryBase[SuspensaoRadar], SuspensaoRadarRepositoryPort
):
    pass
