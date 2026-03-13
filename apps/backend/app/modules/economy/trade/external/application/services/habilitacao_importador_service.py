from __future__ import annotations
from apps.backend.app.modules.economy.trade.external.application.ports import HabilitacaoImportadorRepositoryPort
from apps.backend.app.modules.economy.trade.external.application.services.habilitacao_service_base import HabilitacaoServiceBase
from apps.backend.app.modules.economy.trade.external.domain.models import HabilitacaoImportador
from apps.backend.app.modules.economy.trade.external.exceptions import HabilitacaoImportadorAlreadyExistsError, HabilitacaoImportadorNotFoundError, InvalidHabilitacaoImportadorStateError

class HabilitacaoImportadorService(HabilitacaoServiceBase[HabilitacaoImportador]):

    def __init__(self, *, repository: HabilitacaoImportadorRepositoryPort) -> None:
        super().__init__(repository=repository, domain_cls=HabilitacaoImportador, not_found_error_cls=HabilitacaoImportadorNotFoundError, already_exists_error_cls=HabilitacaoImportadorAlreadyExistsError, invalid_state_error_cls=InvalidHabilitacaoImportadorStateError, entity_label='Habilitacao de Importador')