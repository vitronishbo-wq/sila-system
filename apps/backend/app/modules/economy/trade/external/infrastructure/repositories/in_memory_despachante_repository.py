from __future__ import annotations
from app.modules.economy.trade.external.application.ports import DespachanteRepositoryPort
from app.modules.economy.trade.external.domain.models import Despachante
from app.modules.economy.trade.external.infrastructure.repositories.in_memory_operador_logistico_repository import InMemoryOperadorLogisticoRepository

class InMemoryDespachanteRepository(InMemoryOperadorLogisticoRepository[Despachante], DespachanteRepositoryPort):
    pass