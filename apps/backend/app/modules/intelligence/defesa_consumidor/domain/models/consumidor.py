from dataclasses import dataclass
from typing import Optional

@dataclass
class Consumidor:
    id: int
    nome: str
    email: Optional[str] = None
    telefone: Optional[str] = None