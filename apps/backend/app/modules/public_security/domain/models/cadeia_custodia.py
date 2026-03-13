from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID, uuid4
from apps.backend.app.modules.public_security.domain.enums import StatusCadeiaCustodia

@dataclass
class CadeiaCustodia:
    id: UUID
    codigo_cadeia: str
    prova_id: UUID
    ocorrencia_id: UUID
    status: StatusCadeiaCustodia
    local_atual: str
    responsavel_id: UUID
    data_inicio: datetime
    data_ultima_movimentacao: datetime
    historico_movimentacoes: list[dict]
    integridade_verificada: bool = True
    observacoes: str | None = None
    ativo: bool = True

    @classmethod
    def iniciar(cls, *, codigo_cadeia: str, prova_id: UUID, ocorrencia_id: UUID, local_atual: str, responsavel_id: UUID, observacoes: str | None=None) -> 'CadeiaCustodia':
        now = datetime.now()
        primeira_movimentacao = {'evento': 'inicio', 'timestamp': now.isoformat(), 'local': local_atual.strip(), 'responsavel_id': str(responsavel_id)}
        return cls(id=uuid4(), codigo_cadeia=codigo_cadeia.strip(), prova_id=prova_id, ocorrencia_id=ocorrencia_id, status=StatusCadeiaCustodia.INICIADA, local_atual=local_atual.strip(), responsavel_id=responsavel_id, data_inicio=now, data_ultima_movimentacao=now, historico_movimentacoes=[primeira_movimentacao], integridade_verificada=True, observacoes=observacoes.strip() if observacoes else None, ativo=True)

    def registrar_movimentacao(self, *, status: StatusCadeiaCustodia, local_atual: str, responsavel_id: UUID, observacao: str | None=None) -> None:
        now = datetime.now()
        self.status = status
        self.local_atual = local_atual.strip()
        self.responsavel_id = responsavel_id
        self.data_ultima_movimentacao = now
        self.historico_movimentacoes.append({'evento': 'movimentacao', 'status': status.value, 'timestamp': now.isoformat(), 'local': self.local_atual, 'responsavel_id': str(responsavel_id), 'observacao': observacao.strip() if observacao else None})
        self.ativo = status not in {StatusCadeiaCustodia.ENCERRADA, StatusCadeiaCustodia.ROMPIDA}