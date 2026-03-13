from dataclasses import dataclass

@dataclass(frozen=True)
class NumeroCamisa:
    valor: int

    def __post_init__(self) -> None:
        if not 1 <= self.valor <= 99:
            raise ValueError('Numero da camisa deve estar entre 1 e 99')

    def __str__(self) -> str:
        return str(self.valor)