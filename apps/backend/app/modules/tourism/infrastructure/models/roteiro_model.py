from __future__ import annotations
from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID

@dataclass
class RoteiroModel:
    id: UUID
    codigo: str
    titulo: str
    descricao: str
    municipio_origem: str
    provincia_origem: str
    duracao_horas: int
    pontos_parada: list[str]
    acessivel: bool
    ativo: bool = True
    valor_estimado: Decimal | None = None
    meios_transporte_sugeridos: list[str] | None = None
    parceiros_comerciais: list[str] | None = None
    observacoes: str | None = None