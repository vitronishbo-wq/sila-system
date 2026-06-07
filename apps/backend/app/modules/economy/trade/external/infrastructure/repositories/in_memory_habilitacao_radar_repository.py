from __future__ import annotations

from apps.backend.app.modules.economy.trade.external.application.ports import (
    HabilitacaoRadarRepositoryPort,
)
from apps.backend.app.modules.economy.trade.external.domain.models import HabilitacaoRadar
from apps.backend.app.modules.economy.trade.external.infrastructure.repositories.in_memory_habilitacao_repository_base import (
    InMemoryHabilitacaoRepositoryBase,
)


class InMemoryHabilitacaoRadarRepository(
    InMemoryHabilitacaoRepositoryBase[HabilitacaoRadar], HabilitacaoRadarRepositoryPort
):
    pass
