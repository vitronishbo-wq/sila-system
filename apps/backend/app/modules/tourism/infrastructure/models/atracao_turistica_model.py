from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID

from apps.backend.app.modules.tourism.domain.enums import TipoAtracao


@dataclass
class AtracaoTuristicaModel:
    id: UUID
    codigo: str
    nome: str
    tipo: TipoAtracao
    descricao: str
    endereco: str
    municipio: str
    provincia: str
    horario_funcionamento: str
    acessivel: bool
    ativa: bool = True
    gratuita: bool = False
    capacidade_visitantes_dia: int | None = None
    valor_entrada: Decimal | None = None
    latitude: Decimal | None = None
    longitude: Decimal | None = None
    observacoes: str | None = None
