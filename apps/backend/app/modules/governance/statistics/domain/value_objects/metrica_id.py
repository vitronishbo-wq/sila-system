from dataclasses import dataclass
from apps.backend.app.modules.governance.statistics.exceptions import EstatisticaValidationError

@dataclass(frozen=True)
class MetricaId:
    value: int

    def __post_init__(self) -> None:
        if self.value <= 0:
            raise EstatisticaValidationError('metrica_id deve ser maior que zero')