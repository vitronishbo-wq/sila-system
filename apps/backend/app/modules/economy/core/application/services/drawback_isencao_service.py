from __future__ import annotations

from ....trade.external.application.ports import DrawbackIsencaoRepositoryPort
from ....trade.external.application.services.habilitacao_service_base import HabilitacaoServiceBase
from ....trade.external.domain.models import DrawbackIsencao
from ....trade.external.exceptions import (
    DrawbackIsencaoAlreadyExistsError,
    DrawbackIsencaoNotFoundError,
    InvalidDrawbackIsencaoStateError,
)


class DrawbackIsencaoService(HabilitacaoServiceBase[DrawbackIsencao]):
    def __init__(self, *, repository: DrawbackIsencaoRepositoryPort) -> None:
        super().__init__(
            repository=repository,
            domain_cls=DrawbackIsencao,
            not_found_error_cls=DrawbackIsencaoNotFoundError,
            already_exists_error_cls=DrawbackIsencaoAlreadyExistsError,
            invalid_state_error_cls=InvalidDrawbackIsencaoStateError,
            entity_label="Drawback Isencao",
        )
