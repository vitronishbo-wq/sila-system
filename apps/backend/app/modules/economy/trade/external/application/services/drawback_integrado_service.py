from __future__ import annotations
from apps.backend.app.modules.economy.trade.external.application.ports import DrawbackIntegradoRepositoryPort
from apps.backend.app.modules.economy.trade.external.application.services.habilitacao_service_base import HabilitacaoServiceBase
from apps.backend.app.modules.economy.trade.external.domain.models import DrawbackIntegrado
from apps.backend.app.modules.economy.trade.external.exceptions import DrawbackIntegradoAlreadyExistsError, DrawbackIntegradoNotFoundError, InvalidDrawbackIntegradoStateError

class DrawbackIntegradoService(HabilitacaoServiceBase[DrawbackIntegrado]):

    def __init__(self, *, repository: DrawbackIntegradoRepositoryPort) -> None:
        super().__init__(repository=repository, domain_cls=DrawbackIntegrado, not_found_error_cls=DrawbackIntegradoNotFoundError, already_exists_error_cls=DrawbackIntegradoAlreadyExistsError, invalid_state_error_cls=InvalidDrawbackIntegradoStateError, entity_label='Drawback Integrado')