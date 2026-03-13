from __future__ import annotations
from apps.backend.app.modules.economy.trade.external.application.ports import DrawbackInternoRepositoryPort
from apps.backend.app.modules.economy.trade.external.domain.models import DrawbackInterno
from apps.backend.app.modules.economy.trade.external.infrastructure.repositories.in_memory_habilitacao_repository_base import InMemoryHabilitacaoRepositoryBase

class InMemoryDrawbackInternoRepository(InMemoryHabilitacaoRepositoryBase[DrawbackInterno], DrawbackInternoRepositoryPort):
    pass