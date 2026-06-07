from __future__ import annotations

from ....trade.external.application.ports import HabilitacaoExportadorRepositoryPort
from ....trade.external.application.services.habilitacao_service_base import HabilitacaoServiceBase
from ....trade.external.domain.models import HabilitacaoExportador
from ....trade.external.exceptions import (
    HabilitacaoExportadorAlreadyExistsError,
    HabilitacaoExportadorNotFoundError,
    InvalidHabilitacaoExportadorStateError,
)


class HabilitacaoExportadorService(HabilitacaoServiceBase[HabilitacaoExportador]):
    def __init__(self, *, repository: HabilitacaoExportadorRepositoryPort) -> None:
        super().__init__(
            repository=repository,
            domain_cls=HabilitacaoExportador,
            not_found_error_cls=HabilitacaoExportadorNotFoundError,
            already_exists_error_cls=HabilitacaoExportadorAlreadyExistsError,
            invalid_state_error_cls=InvalidHabilitacaoExportadorStateError,
            entity_label="Habilitacao de Exportador",
        )
