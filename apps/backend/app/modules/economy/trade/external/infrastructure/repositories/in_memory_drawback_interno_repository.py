from __future__ import annotations
from app.modules.economy.trade.external.application.ports import DrawbackInternoRepositoryPort
from app.modules.economy.trade.external.domain.models import DrawbackInterno
from app.modules.economy.trade.external.infrastructure.repositories.in_memory_habilitacao_repository_base import InMemoryHabilitacaoRepositoryBase

class InMemoryDrawbackInternoRepository(InMemoryHabilitacaoRepositoryBase[DrawbackInterno], DrawbackInternoRepositoryPort):
    pass