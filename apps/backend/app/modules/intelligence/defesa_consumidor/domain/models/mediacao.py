from dataclasses import dataclass
from datetime import datetime

from apps.backend.app.modules.intelligence.defesa_consumidor.domain.enums import StatusMediacao


@dataclass
class Mediacao:
    id: int | None
    reclamacao_id: int
    status: StatusMediacao = StatusMediacao.AGENDADA
    data_inicio: datetime | None = None
    data_fim: datetime | None = None
