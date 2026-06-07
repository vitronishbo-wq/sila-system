from __future__ import annotations

from ....trade.external.application.ports import DrawbackSubstituicaoRepositoryPort
from ....trade.external.application.services.habilitacao_service_base import HabilitacaoServiceBase
from ....trade.external.domain.models import DrawbackSubstituicao
from ....trade.external.exceptions import (
    DrawbackSubstituicaoAlreadyExistsError,
    DrawbackSubstituicaoNotFoundError,
    InvalidDrawbackSubstituicaoStateError,
)


class DrawbackSubstituicaoService(HabilitacaoServiceBase[DrawbackSubstituicao]):
    def __init__(self, *, repository: DrawbackSubstituicaoRepositoryPort) -> None:
        super().__init__(
            repository=repository,
            domain_cls=DrawbackSubstituicao,
            not_found_error_cls=DrawbackSubstituicaoNotFoundError,
            already_exists_error_cls=DrawbackSubstituicaoAlreadyExistsError,
            invalid_state_error_cls=InvalidDrawbackSubstituicaoStateError,
            entity_label="Drawback Substituicao",
        )
