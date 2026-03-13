from __future__ import annotations
from app.modules.economy.trade.external.application.ports import DespachanteRepositoryPort
from app.modules.economy.trade.external.application.services.operador_logistico_service_base import OperadorLogisticoServiceBase
from app.modules.economy.trade.external.domain.models import Despachante
from app.modules.economy.trade.external.exceptions import DespachanteAlreadyExistsError, DespachanteNotFoundError, InvalidDespachanteStateError

class DespachanteService(OperadorLogisticoServiceBase[Despachante]):

    def __init__(self, *, repository: DespachanteRepositoryPort) -> None:
        super().__init__(repository=repository, domain_cls=Despachante, not_found_error_cls=DespachanteNotFoundError, already_exists_error_cls=DespachanteAlreadyExistsError, invalid_state_error_cls=InvalidDespachanteStateError, entity_label='Despachante')