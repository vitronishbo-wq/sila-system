from __future__ import annotations
from ....trade.external.application.ports import HabilitacaoRadarRepositoryPort
from ....trade.external.application.services.habilitacao_service_base import HabilitacaoServiceBase
from ....trade.external.domain.models import HabilitacaoRadar
from ....trade.external.exceptions import HabilitacaoRadarAlreadyExistsError, HabilitacaoRadarNotFoundError, InvalidHabilitacaoRadarStateError

class HabilitacaoRadarService(HabilitacaoServiceBase[HabilitacaoRadar]):

    def __init__(self, *, repository: HabilitacaoRadarRepositoryPort) -> None:
        super().__init__(repository=repository, domain_cls=HabilitacaoRadar, not_found_error_cls=HabilitacaoRadarNotFoundError, already_exists_error_cls=HabilitacaoRadarAlreadyExistsError, invalid_state_error_cls=InvalidHabilitacaoRadarStateError, entity_label='Habilitacao de Radar')