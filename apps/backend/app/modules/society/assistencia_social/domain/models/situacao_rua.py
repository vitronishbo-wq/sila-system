from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID, uuid4
from app.modules.society.assistencia_social.domain.enums import StatusAcompanhamento

@dataclass
class SituacaoRua:
    id: UUID
    codigo: str
    beneficiario_id: UUID
    data_registro: datetime
    localizacao: str
    motivo: str
    status: StatusAcompanhamento

    @classmethod
    def registrar(cls, *, codigo: str, beneficiario_id: UUID, localizacao: str, motivo: str) -> 'SituacaoRua':
        return cls(id=uuid4(), codigo=codigo, beneficiario_id=beneficiario_id, data_registro=datetime.utcnow(), localizacao=localizacao, motivo=motivo, status=StatusAcompanhamento.ATIVO)

    def encerrar(self) -> None:
        self.status = StatusAcompanhamento.ENCERRADO