from dataclasses import dataclass


@dataclass
class Estabelecimento:
    id: int
    nome_fantasia: str
    nif: str | None = None
