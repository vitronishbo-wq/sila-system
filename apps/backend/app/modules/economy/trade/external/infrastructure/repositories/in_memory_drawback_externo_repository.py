from __future__ import annotations
from apps.backend.app.modules.economy.trade.external.application.ports import DrawbackExternoRepositoryPort
from apps.backend.app.modules.economy.trade.external.domain.models import DrawbackExterno
from apps.backend.app.modules.economy.trade.external.infrastructure.repositories.in_memory_habilitacao_repository_base import InMemoryHabilitacaoRepositoryBase

class InMemoryDrawbackExternoRepository(InMemoryHabilitacaoRepositoryBase[DrawbackExterno], DrawbackExternoRepositoryPort):
    pass