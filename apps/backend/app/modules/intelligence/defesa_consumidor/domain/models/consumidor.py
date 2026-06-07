from dataclasses import dataclass


@dataclass
class Consumidor:
    id: int
    nome: str
    email: str | None = None
    telefone: str | None = None
