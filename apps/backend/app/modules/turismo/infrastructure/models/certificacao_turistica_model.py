from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID


@dataclass
class CertificacaoTuristicaModel:
    id: UUID
    nome: str
