from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from uuid import UUID, uuid4

from apps.backend.app.modules.resources.florestas.domain.enums import TipoOperadorFlorestal


@dataclass
class ConcessionarioFlorestal:
    id: UUID
    nome: str
    nif: str
    tipo_operador: TipoOperadorFlorestal
    data_registro: date
    ativo: bool = True
    observacoes: str | None = None

    @classmethod
    def cadastrar(
        cls,
        *,
        nome: str,
        nif: str,
        tipo_operador: TipoOperadorFlorestal = TipoOperadorFlorestal.EMPRESA,
    ) -> ConcessionarioFlorestal:
        return cls(
            id=uuid4(), nome=nome, nif=nif, tipo_operador=tipo_operador, data_registro=date.today()
        )
