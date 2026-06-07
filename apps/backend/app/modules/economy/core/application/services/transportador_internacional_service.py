from __future__ import annotations

from ....trade.external.application.ports import TransportadorInternacionalRepositoryPort
from ....trade.external.application.services.operador_logistico_service_base import (
    OperadorLogisticoServiceBase,
)
from ....trade.external.domain.models import TransportadorInternacional
from ....trade.external.exceptions import (
    InvalidTransportadorInternacionalStateError,
    TransportadorInternacionalAlreadyExistsError,
    TransportadorInternacionalNotFoundError,
)


class TransportadorInternacionalService(OperadorLogisticoServiceBase[TransportadorInternacional]):
    def __init__(self, *, repository: TransportadorInternacionalRepositoryPort) -> None:
        super().__init__(
            repository=repository,
            domain_cls=TransportadorInternacional,
            not_found_error_cls=TransportadorInternacionalNotFoundError,
            already_exists_error_cls=TransportadorInternacionalAlreadyExistsError,
            invalid_state_error_cls=InvalidTransportadorInternacionalStateError,
            entity_label="Transportador Internacional",
        )
