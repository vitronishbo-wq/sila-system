from __future__ import annotations
from apps.backend.app.modules.economy.trade.external.application.ports import DrawbackIntegradoRepositoryPort
from apps.backend.app.modules.economy.trade.external.domain.models import DrawbackIntegrado
from apps.backend.app.modules.economy.trade.external.infrastructure.repositories.in_memory_habilitacao_repository_base import InMemoryHabilitacaoRepositoryBase

class InMemoryDrawbackIntegradoRepository(InMemoryHabilitacaoRepositoryBase[DrawbackIntegrado], DrawbackIntegradoRepositoryPort):
    pass