from __future__ import annotations

from apps.backend.app.modules.economy.trade.external.application.ports import (
    DrawbackInternoRepositoryPort,
)
from apps.backend.app.modules.economy.trade.external.application.services.habilitacao_service_base import (
    HabilitacaoServiceBase,
)
from apps.backend.app.modules.economy.trade.external.domain.models import DrawbackInterno
from apps.backend.app.modules.economy.trade.external.exceptions import (
    DrawbackInternoAlreadyExistsError,
    DrawbackInternoNotFoundError,
    InvalidDrawbackInternoStateError,
)


class DrawbackInternoService(HabilitacaoServiceBase[DrawbackInterno]):
    def __init__(self, *, repository: DrawbackInternoRepositoryPort) -> None:
        super().__init__(
            repository=repository,
            domain_cls=DrawbackInterno,
            not_found_error_cls=DrawbackInternoNotFoundError,
            already_exists_error_cls=DrawbackInternoAlreadyExistsError,
            invalid_state_error_cls=InvalidDrawbackInternoStateError,
            entity_label="Drawback Interno",
        )
