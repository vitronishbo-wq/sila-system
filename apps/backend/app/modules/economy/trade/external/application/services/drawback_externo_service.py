from __future__ import annotations
from app.modules.economy.trade.external.application.ports import DrawbackExternoRepositoryPort
from app.modules.economy.trade.external.application.services.habilitacao_service_base import HabilitacaoServiceBase
from app.modules.economy.trade.external.domain.models import DrawbackExterno
from app.modules.economy.trade.external.exceptions import DrawbackExternoAlreadyExistsError, DrawbackExternoNotFoundError, InvalidDrawbackExternoStateError

class DrawbackExternoService(HabilitacaoServiceBase[DrawbackExterno]):

    def __init__(self, *, repository: DrawbackExternoRepositoryPort) -> None:
        super().__init__(repository=repository, domain_cls=DrawbackExterno, not_found_error_cls=DrawbackExternoNotFoundError, already_exists_error_cls=DrawbackExternoAlreadyExistsError, invalid_state_error_cls=InvalidDrawbackExternoStateError, entity_label='Drawback Externo')