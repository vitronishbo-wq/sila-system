from __future__ import annotations
from ....trade.external.application.ports import RadarRepositoryPort
from ....trade.external.application.services.operador_logistico_service_base import OperadorLogisticoServiceBase
from ....trade.external.domain.models import Radar
from ....trade.external.exceptions import InvalidRadarStateError, RadarAlreadyExistsError, RadarNotFoundError

class RadarService(OperadorLogisticoServiceBase[Radar]):

    def __init__(self, *, repository: RadarRepositoryPort) -> None:
        super().__init__(repository=repository, domain_cls=Radar, not_found_error_cls=RadarNotFoundError, already_exists_error_cls=RadarAlreadyExistsError, invalid_state_error_cls=InvalidRadarStateError, entity_label='Radar')