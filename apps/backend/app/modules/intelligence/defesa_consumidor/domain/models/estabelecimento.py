from dataclasses import dataclass
from typing import Optional

@dataclass
class Estabelecimento:
    id: int
    nome_fantasia: str
    nif: Optional[str] = None