from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID, uuid4
from apps.backend.app.modules.society.assistencia_social.domain.enums import StatusAcompanhamento

@dataclass
class CriancaRisco:
    id: UUID
    codigo: str
    beneficiario_id: UUID
    citizen_id_crianca: UUID
    idade: int
    motivo: str
    escolarizada: bool
    data_registro: datetime
    status: StatusAcompanhamento

    @classmethod
    def registrar(cls, *, codigo: str, beneficiario_id: UUID, citizen_id_crianca: UUID, idade: int, motivo: str, escolarizada: bool) -> 'CriancaRisco':
        return cls(id=uuid4(), codigo=codigo, beneficiario_id=beneficiario_id, citizen_id_crianca=citizen_id_crianca, idade=idade, motivo=motivo, escolarizada=escolarizada, data_registro=datetime.utcnow(), status=StatusAcompanhamento.ATIVO)

    def encerrar_acompanhamento(self) -> None:
        self.status = StatusAcompanhamento.ENCERRADO