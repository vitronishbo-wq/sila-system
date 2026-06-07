from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from uuid import UUID, uuid4

from apps.backend.app.modules.resources.pescas.domain.enums import TipoPescador


@dataclass
class Pescador:
    id: UUID
    nome: str
    numero_registro: str
    tipo: TipoPescador
    citizen_id: UUID
    data_registro: date
    ativo: bool = True
    telefone: str | None = None
    email: str | None = None
    cooperativa_id: UUID | None = None
    observacoes: str | None = None

    @classmethod
    def cadastrar(
        cls, *, nome: str, numero_registro: str, tipo: TipoPescador, citizen_id: UUID
    ) -> Pescador:
        return cls(
            id=uuid4(),
            nome=nome,
            numero_registro=numero_registro,
            tipo=tipo,
            citizen_id=citizen_id,
            data_registro=date.today(),
        )
