from __future__ import annotations
from app.modules.economy.trade.external.application.ports import DrawbackExternoRepositoryPort
from app.modules.economy.trade.external.domain.models import DrawbackExterno
from app.modules.economy.trade.external.infrastructure.repositories.in_memory_habilitacao_repository_base import InMemoryHabilitacaoRepositoryBase

class InMemoryDrawbackExternoRepository(InMemoryHabilitacaoRepositoryBase[DrawbackExterno], DrawbackExternoRepositoryPort):
    pass