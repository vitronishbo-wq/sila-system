from __future__ import annotations
from ....trade.external.application.ports import SiscomexDrawbackRepositoryPort
from ....trade.external.application.services.habilitacao_service_base import HabilitacaoServiceBase
from ....trade.external.domain.models import SiscomexDrawback
from ....trade.external.exceptions import InvalidSiscomexDrawbackStateError, SiscomexDrawbackAlreadyExistsError, SiscomexDrawbackNotFoundError

class SiscomexDrawbackService(HabilitacaoServiceBase[SiscomexDrawback]):

    def __init__(self, *, repository: SiscomexDrawbackRepositoryPort) -> None:
        super().__init__(repository=repository, domain_cls=SiscomexDrawback, not_found_error_cls=SiscomexDrawbackNotFoundError, already_exists_error_cls=SiscomexDrawbackAlreadyExistsError, invalid_state_error_cls=InvalidSiscomexDrawbackStateError, entity_label='Siscomex Drawback')