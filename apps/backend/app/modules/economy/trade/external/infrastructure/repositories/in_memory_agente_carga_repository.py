from __future__ import annotations

from apps.backend.app.modules.economy.trade.external.application.ports import (
    AgenteCargaRepositoryPort,
)
from apps.backend.app.modules.economy.trade.external.domain.models import AgenteCarga
from apps.backend.app.modules.economy.trade.external.infrastructure.repositories.in_memory_operador_logistico_repository import (
    InMemoryOperadorLogisticoRepository,
)


class InMemoryAgenteCargaRepository(
    InMemoryOperadorLogisticoRepository[AgenteCarga], AgenteCargaRepositoryPort
):
    pass
