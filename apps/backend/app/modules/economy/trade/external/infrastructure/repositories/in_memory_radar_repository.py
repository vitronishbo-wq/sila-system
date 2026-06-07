from __future__ import annotations

from apps.backend.app.modules.economy.trade.external.application.ports import RadarRepositoryPort
from apps.backend.app.modules.economy.trade.external.domain.models import Radar
from apps.backend.app.modules.economy.trade.external.infrastructure.repositories.in_memory_operador_logistico_repository import (
    InMemoryOperadorLogisticoRepository,
)


class InMemoryRadarRepository(InMemoryOperadorLogisticoRepository[Radar], RadarRepositoryPort):
    pass
