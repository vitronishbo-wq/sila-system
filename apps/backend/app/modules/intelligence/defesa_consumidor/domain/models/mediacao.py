from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from apps.backend.app.modules.intelligence.defesa_consumidor.domain.enums import StatusMediacao

@dataclass
class Mediacao:
    id: Optional[int]
    reclamacao_id: int
    status: StatusMediacao = StatusMediacao.AGENDADA
    data_inicio: Optional[datetime] = None
    data_fim: Optional[datetime] = None