from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

@dataclass
class FiscalizacaoPesca:
    id: UUID
    embarcacao_id: UUID
    data_fiscalizacao: datetime
    local: str
    agente: str
    regular: bool
    observacoes: Optional[str] = None

    @classmethod
    def registrar(cls, *, embarcacao_id: UUID, local: str, agente: str, regular: bool, observacoes: Optional[str]=None) -> 'FiscalizacaoPesca':
        return cls(id=uuid4(), embarcacao_id=embarcacao_id, data_fiscalizacao=datetime.utcnow(), local=local, agente=agente, regular=regular, observacoes=observacoes)