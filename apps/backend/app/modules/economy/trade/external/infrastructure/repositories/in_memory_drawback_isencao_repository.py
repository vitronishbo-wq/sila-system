from __future__ import annotations
from app.modules.economy.trade.external.application.ports import DrawbackIsencaoRepositoryPort
from app.modules.economy.trade.external.domain.models import DrawbackIsencao
from app.modules.economy.trade.external.infrastructure.repositories.in_memory_habilitacao_repository_base import InMemoryHabilitacaoRepositoryBase

class InMemoryDrawbackIsencaoRepository(InMemoryHabilitacaoRepositoryBase[DrawbackIsencao], DrawbackIsencaoRepositoryPort):
    pass