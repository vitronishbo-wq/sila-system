from __future__ import annotations
from apps.backend.app.modules.economy.trade.external.application.ports import SuspensaoRadarRepositoryPort
from apps.backend.app.modules.economy.trade.external.application.services.habilitacao_service_base import HabilitacaoServiceBase
from apps.backend.app.modules.economy.trade.external.domain.models import SuspensaoRadar
from apps.backend.app.modules.economy.trade.external.exceptions import InvalidSuspensaoRadarStateError, SuspensaoRadarAlreadyExistsError, SuspensaoRadarNotFoundError

class SuspensaoRadarService(HabilitacaoServiceBase[SuspensaoRadar]):

    def __init__(self, *, repository: SuspensaoRadarRepositoryPort) -> None:
        super().__init__(repository=repository, domain_cls=SuspensaoRadar, not_found_error_cls=SuspensaoRadarNotFoundError, already_exists_error_cls=SuspensaoRadarAlreadyExistsError, invalid_state_error_cls=InvalidSuspensaoRadarStateError, entity_label='Suspensao de Radar')