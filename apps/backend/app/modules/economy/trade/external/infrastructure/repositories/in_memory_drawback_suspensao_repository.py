from __future__ import annotations

from apps.backend.app.modules.economy.trade.external.application.ports import (
    DrawbackSuspensaoRepositoryPort,
)
from apps.backend.app.modules.economy.trade.external.domain.models import DrawbackSuspensao
from apps.backend.app.modules.economy.trade.external.infrastructure.repositories.in_memory_habilitacao_repository_base import (
    InMemoryHabilitacaoRepositoryBase,
)


class InMemoryDrawbackSuspensaoRepository(
    InMemoryHabilitacaoRepositoryBase[DrawbackSuspensao], DrawbackSuspensaoRepositoryPort
):
    pass
