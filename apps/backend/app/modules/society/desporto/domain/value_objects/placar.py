from dataclasses import dataclass

@dataclass(frozen=True)
class Placar:
    casa: int
    fora: int

    def __post_init__(self) -> None:
        if self.casa < 0 or self.fora < 0:
            raise ValueError('Placar nao pode conter valores negativos')

    def __str__(self) -> str:
        return f'{self.casa} - {self.fora}'