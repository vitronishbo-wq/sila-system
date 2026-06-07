from __future__ import annotations

from apps.backend.app.modules.economy.trade.external.application.ports import (
    DrawbackRestituicaoRepositoryPort,
)
from apps.backend.app.modules.economy.trade.external.domain.models import DrawbackRestituicao
from apps.backend.app.modules.economy.trade.external.infrastructure.repositories.in_memory_habilitacao_repository_base import (
    InMemoryHabilitacaoRepositoryBase,
)


class InMemoryDrawbackRestituicaoRepository(
    InMemoryHabilitacaoRepositoryBase[DrawbackRestituicao], DrawbackRestituicaoRepositoryPort
):
    pass
