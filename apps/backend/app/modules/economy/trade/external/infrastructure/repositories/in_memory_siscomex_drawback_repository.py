from __future__ import annotations

from apps.backend.app.modules.economy.trade.external.application.ports import (
    SiscomexDrawbackRepositoryPort,
)
from apps.backend.app.modules.economy.trade.external.domain.models import SiscomexDrawback
from apps.backend.app.modules.economy.trade.external.infrastructure.repositories.in_memory_habilitacao_repository_base import (
    InMemoryHabilitacaoRepositoryBase,
)


class InMemorySiscomexDrawbackRepository(
    InMemoryHabilitacaoRepositoryBase[SiscomexDrawback], SiscomexDrawbackRepositoryPort
):
    pass
