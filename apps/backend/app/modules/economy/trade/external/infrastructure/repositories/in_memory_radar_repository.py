from __future__ import annotations
from app.modules.economy.trade.external.application.ports import RadarRepositoryPort
from app.modules.economy.trade.external.domain.models import Radar
from app.modules.economy.trade.external.infrastructure.repositories.in_memory_operador_logistico_repository import InMemoryOperadorLogisticoRepository

class InMemoryRadarRepository(InMemoryOperadorLogisticoRepository[Radar], RadarRepositoryPort):
    pass