from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from uuid import UUID
from apps.backend.app.modules.resources.aguas_saneamento.domain.enums import StatusAbastecimento

@dataclass
class AbastecimentoModel:
    id: UUID
    codigo_abastecimento: str
    infraestrutura_id: UUID
    nome_sistema: str
    provincia: str
    municipio: str
    status: StatusAbastecimento
    data_registro: date