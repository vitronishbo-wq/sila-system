from dataclasses import dataclass
from datetime import datetime
from app.modules.governance.statistics.exceptions import EstatisticaValidationError

@dataclass(frozen=True)
class Periodo:
    inicio: datetime
    fim: datetime

    def __post_init__(self) -> None:
        if self.fim < self.inicio:
            raise EstatisticaValidationError('fim nao pode ser anterior ao inicio')