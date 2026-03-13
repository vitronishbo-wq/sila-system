from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from apps.backend.app.modules.intelligence.defesa_consumidor.domain.enums import TipoSancao

@dataclass
class Sancao:
    id: Optional[int]
    reclamacao_id: int
    tipo: TipoSancao
    descricao: str
    valor_multa: Optional[float] = None
    data_aplicacao: datetime = field(default_factory=datetime.utcnow)