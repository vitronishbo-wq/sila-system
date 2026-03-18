from __future__ import annotations
from ....trade.external.application.ports import DrawbackInternoRepositoryPort
from ....trade.external.application.services.habilitacao_service_base import HabilitacaoServiceBase
from ....trade.external.domain.models import DrawbackInterno
from ....trade.external.exceptions import DrawbackInternoAlreadyExistsError, DrawbackInternoNotFoundError, InvalidDrawbackInternoStateError

class DrawbackInternoService(HabilitacaoServiceBase[DrawbackInterno]):

    def __init__(self, *, repository: DrawbackInternoRepositoryPort) -> None:
        super().__init__(repository=repository, domain_cls=DrawbackInterno, not_found_error_cls=DrawbackInternoNotFoundError, already_exists_error_cls=DrawbackInternoAlreadyExistsError, invalid_state_error_cls=InvalidDrawbackInternoStateError, entity_label='Drawback Interno')