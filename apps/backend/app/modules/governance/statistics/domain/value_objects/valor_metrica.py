from dataclasses import dataclass

from apps.backend.app.modules.governance.statistics.exceptions import EstatisticaValidationError


@dataclass(frozen=True)
class ValorMetrica:
    value: float

    def __post_init__(self) -> None:
        if self.value != self.value:
            raise EstatisticaValidationError("valor da metrica nao pode ser NaN")
