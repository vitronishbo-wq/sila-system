from __future__ import annotations
from apps.backend.app.modules.economy.trade.external.application.ports import CancelamentoRadarRepositoryPort
from apps.backend.app.modules.economy.trade.external.domain.models import CancelamentoRadar
from apps.backend.app.modules.economy.trade.external.infrastructure.repositories.in_memory_habilitacao_repository_base import InMemoryHabilitacaoRepositoryBase

class InMemoryCancelamentoRadarRepository(InMemoryHabilitacaoRepositoryBase[CancelamentoRadar], CancelamentoRadarRepositoryPort):
    pass