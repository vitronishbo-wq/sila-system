from __future__ import annotations
from ....trade.external.application.ports import DrawbackVerdeAmareloRepositoryPort
from ....trade.external.application.services.habilitacao_service_base import HabilitacaoServiceBase
from ....trade.external.domain.models import DrawbackVerdeAmarelo
from ....trade.external.exceptions import DrawbackVerdeAmareloAlreadyExistsError, DrawbackVerdeAmareloNotFoundError, InvalidDrawbackVerdeAmareloStateError

class DrawbackVerdeAmareloService(HabilitacaoServiceBase[DrawbackVerdeAmarelo]):

    def __init__(self, *, repository: DrawbackVerdeAmareloRepositoryPort) -> None:
        super().__init__(repository=repository, domain_cls=DrawbackVerdeAmarelo, not_found_error_cls=DrawbackVerdeAmareloNotFoundError, already_exists_error_cls=DrawbackVerdeAmareloAlreadyExistsError, invalid_state_error_cls=InvalidDrawbackVerdeAmareloStateError, entity_label='Drawback Verde Amarelo')