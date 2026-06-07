from __future__ import annotations

from ....trade.external.application.ports import DrawbackRestituicaoRepositoryPort
from ....trade.external.application.services.habilitacao_service_base import HabilitacaoServiceBase
from ....trade.external.domain.models import DrawbackRestituicao
from ....trade.external.exceptions import (
    DrawbackRestituicaoAlreadyExistsError,
    DrawbackRestituicaoNotFoundError,
    InvalidDrawbackRestituicaoStateError,
)


class DrawbackRestituicaoService(HabilitacaoServiceBase[DrawbackRestituicao]):
    def __init__(self, *, repository: DrawbackRestituicaoRepositoryPort) -> None:
        super().__init__(
            repository=repository,
            domain_cls=DrawbackRestituicao,
            not_found_error_cls=DrawbackRestituicaoNotFoundError,
            already_exists_error_cls=DrawbackRestituicaoAlreadyExistsError,
            invalid_state_error_cls=InvalidDrawbackRestituicaoStateError,
            entity_label="Drawback Restituicao",
        )
