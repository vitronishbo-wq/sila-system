from __future__ import annotations

from apps.backend.app.modules.economy.trade.external.application.ports import DrawbackRepositoryPort
from apps.backend.app.modules.economy.trade.external.application.services.operador_logistico_service_base import (
    OperadorLogisticoServiceBase,
)
from apps.backend.app.modules.economy.trade.external.domain.models import Drawback
from apps.backend.app.modules.economy.trade.external.exceptions import (
    DrawbackAlreadyExistsError,
    DrawbackNotFoundError,
    InvalidDrawbackStateError,
)


class DrawbackService(OperadorLogisticoServiceBase[Drawback]):
    def __init__(self, *, repository: DrawbackRepositoryPort) -> None:
        super().__init__(
            repository=repository,
            domain_cls=Drawback,
            not_found_error_cls=DrawbackNotFoundError,
            already_exists_error_cls=DrawbackAlreadyExistsError,
            invalid_state_error_cls=InvalidDrawbackStateError,
            entity_label="Drawback",
        )
