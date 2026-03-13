from __future__ import annotations
from app.modules.economy.trade.external.application.ports import TransportadorInternacionalRepositoryPort
from app.modules.economy.trade.external.application.services.operador_logistico_service_base import OperadorLogisticoServiceBase
from app.modules.economy.trade.external.domain.models import TransportadorInternacional
from app.modules.economy.trade.external.exceptions import InvalidTransportadorInternacionalStateError, TransportadorInternacionalAlreadyExistsError, TransportadorInternacionalNotFoundError

class TransportadorInternacionalService(OperadorLogisticoServiceBase[TransportadorInternacional]):

    def __init__(self, *, repository: TransportadorInternacionalRepositoryPort) -> None:
        super().__init__(repository=repository, domain_cls=TransportadorInternacional, not_found_error_cls=TransportadorInternacionalNotFoundError, already_exists_error_cls=TransportadorInternacionalAlreadyExistsError, invalid_state_error_cls=InvalidTransportadorInternacionalStateError, entity_label='Transportador Internacional')