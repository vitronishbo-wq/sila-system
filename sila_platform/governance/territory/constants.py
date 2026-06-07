from __future__ import annotations

from enum import Enum


SCOPE_ORDER = ["nacional", "provincial", "municipal", "unidade", "operador"]


class NivelTerritorial(str, Enum):
    NACIONAL = "nacional"
    PROVINCIAL = "provincial"
    MUNICIPAL = "municipal"
    UNIDADE = "unidade"
    OPERADOR = "operador"


@staticmethod
def nivel_index(nivel: str) -> int:
    return SCOPE_ORDER.index(nivel) if nivel in SCOPE_ORDER else 0
