from __future__ import annotations
from app.modules.economy.trade.external.application.ports import DrawbackRepositoryPort
from app.modules.economy.trade.external.domain.models import Drawback
from app.modules.economy.trade.external.infrastructure.repositories.in_memory_operador_logistico_repository import InMemoryOperadorLogisticoRepository

class InMemoryDrawbackRepository(InMemoryOperadorLogisticoRepository[Drawback], DrawbackRepositoryPort):
    pass