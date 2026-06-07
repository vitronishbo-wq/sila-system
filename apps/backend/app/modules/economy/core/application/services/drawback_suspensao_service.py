from __future__ import annotations

from ....trade.external.application.ports import DrawbackSuspensaoRepositoryPort
from ....trade.external.application.services.habilitacao_service_base import HabilitacaoServiceBase
from ....trade.external.domain.models import DrawbackSuspensao
from ....trade.external.exceptions import (
    DrawbackSuspensaoAlreadyExistsError,
    DrawbackSuspensaoNotFoundError,
    InvalidDrawbackSuspensaoStateError,
)


class DrawbackSuspensaoService(HabilitacaoServiceBase[DrawbackSuspensao]):
    def __init__(self, *, repository: DrawbackSuspensaoRepositoryPort) -> None:
        super().__init__(
            repository=repository,
            domain_cls=DrawbackSuspensao,
            not_found_error_cls=DrawbackSuspensaoNotFoundError,
            already_exists_error_cls=DrawbackSuspensaoAlreadyExistsError,
            invalid_state_error_cls=InvalidDrawbackSuspensaoStateError,
            entity_label="Drawback Suspensao",
        )
