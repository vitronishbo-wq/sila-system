from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID, uuid4
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.domain.enums import StatusReclamacaoTelecom, TipoReclamacaoTelecom

@dataclass
class Reclamacao:
    id: UUID
    protocolo: str
    assinante_id: UUID
    tipo: TipoReclamacaoTelecom
    descricao: str
    prioridade: str
    status: StatusReclamacaoTelecom
    data_abertura: datetime
    data_fechamento: datetime | None = None
    resposta: str | None = None

    @classmethod
    def abrir(cls, *, assinante_id: UUID, tipo: TipoReclamacaoTelecom, descricao: str, prioridade: str) -> 'Reclamacao':
        if not descricao.strip():
            raise ValueError('Descricao obrigatoria')
        return cls(id=uuid4(), protocolo='', assinante_id=assinante_id, tipo=tipo, descricao=descricao.strip(), prioridade=prioridade.strip().lower(), status=StatusReclamacaoTelecom.ABERTA, data_abertura=datetime.utcnow())

    def fechar(self, *, resposta: str) -> None:
        if self.status == StatusReclamacaoTelecom.FECHADA:
            raise ValueError('Reclamacao ja fechada')
        self.status = StatusReclamacaoTelecom.FECHADA
        self.data_fechamento = datetime.utcnow()
        self.resposta = resposta.strip()