from __future__ import annotations

from ....trade.external.application.ports import HabilitacaoImportadorRepositoryPort
from ....trade.external.application.services.habilitacao_service_base import HabilitacaoServiceBase
from ....trade.external.domain.models import HabilitacaoImportador
from ....trade.external.exceptions import (
    HabilitacaoImportadorAlreadyExistsError,
    HabilitacaoImportadorNotFoundError,
    InvalidHabilitacaoImportadorStateError,
)


class HabilitacaoImportadorService(HabilitacaoServiceBase[HabilitacaoImportador]):
    def __init__(self, *, repository: HabilitacaoImportadorRepositoryPort) -> None:
        super().__init__(
            repository=repository,
            domain_cls=HabilitacaoImportador,
            not_found_error_cls=HabilitacaoImportadorNotFoundError,
            already_exists_error_cls=HabilitacaoImportadorAlreadyExistsError,
            invalid_state_error_cls=InvalidHabilitacaoImportadorStateError,
            entity_label="Habilitacao de Importador",
        )
