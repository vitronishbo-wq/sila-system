from __future__ import annotations

from apps.backend.app.modules.economy.trade.external.application.ports import (
    AgenteCargaRepositoryPort,
)
from apps.backend.app.modules.economy.trade.external.application.services.operador_logistico_service_base import (
    OperadorLogisticoServiceBase,
)
from apps.backend.app.modules.economy.trade.external.domain.models import AgenteCarga
from apps.backend.app.modules.economy.trade.external.exceptions import (
    AgenteCargaAlreadyExistsError,
    AgenteCargaNotFoundError,
    InvalidAgenteCargaStateError,
)


class AgenteCargaService(OperadorLogisticoServiceBase[AgenteCarga]):
    def __init__(self, *, repository: AgenteCargaRepositoryPort) -> None:
        super().__init__(
            repository=repository,
            domain_cls=AgenteCarga,
            not_found_error_cls=AgenteCargaNotFoundError,
            already_exists_error_cls=AgenteCargaAlreadyExistsError,
            invalid_state_error_cls=InvalidAgenteCargaStateError,
            entity_label="Agente de Carga",
        )
