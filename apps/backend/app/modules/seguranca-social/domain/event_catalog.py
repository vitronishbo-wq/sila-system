from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from decimal import Decimal
from typing import Any
from uuid import UUID, uuid4


@dataclass
class EmpregadorRegistado:
    event_type: str = "empregador_registado"
    version: int = 1
    empregador_id: UUID | None = None
    nif: str = ""
    nome_empresa: str = ""
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    event_id: UUID = field(default_factory=uuid4)
    metadata: dict[str, Any] = field(default_factory=dict)
    correlation_id: UUID | None = None


@dataclass
class ContribuicaoRecebida:
    event_type: str = "contribuicao_recebida"
    version: int = 1
    contribuicao_id: UUID | None = None
    empregador_id: UUID | None = None
    cidadao_id: UUID | None = None
    valor: Decimal = Decimal("0")
    mes_comp: str = ""
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    event_id: UUID = field(default_factory=uuid4)
    metadata: dict[str, Any] = field(default_factory=dict)
    correlation_id: UUID | None = None


@dataclass
class BeneficioAtribuido:
    event_type: str = "beneficio_atribuido"
    version: int = 1
    beneficio_id: UUID | None = None
    cidadao_id: UUID | None = None
    tipo_beneficio: str = ""
    valor: Decimal = Decimal("0")
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    event_id: UUID = field(default_factory=uuid4)
    metadata: dict[str, Any] = field(default_factory=dict)
    correlation_id: UUID | None = None


EVENT_CATALOG = {
    "empregador_registado": EmpregadorRegistado,
    "contribuicao_recebida": ContribuicaoRecebida,
    "beneficio_atribuido": BeneficioAtribuido,
}
