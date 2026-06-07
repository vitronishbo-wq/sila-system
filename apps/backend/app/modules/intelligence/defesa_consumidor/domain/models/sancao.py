from dataclasses import dataclass, field
from datetime import datetime

from apps.backend.app.modules.intelligence.defesa_consumidor.domain.enums import TipoSancao


@dataclass
class Sancao:
    id: int | None
    reclamacao_id: int
    tipo: TipoSancao
    descricao: str
    valor_multa: float | None = None
    data_aplicacao: datetime = field(default_factory=datetime.utcnow)
