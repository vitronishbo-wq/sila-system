from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from uuid import UUID, uuid4
from apps.backend.app.modules.public_security.domain.enums import StatusInvestigacao

@dataclass
class Investigacao:
    id: UUID
    codigo_investigacao: str
    ocorrencia_id: UUID
    unidade_id: UUID
    data_abertura: date
    status: StatusInvestigacao
    delegado_responsavel_id: UUID | None = None
    data_conclusao: date | None = None
    resumo: str | None = None
    observacoes: str | None = None
    ativo: bool = True

    @classmethod
    def abrir(cls, *, codigo_investigacao: str, ocorrencia_id: UUID, unidade_id: UUID, delegado_responsavel_id: UUID | None=None, resumo: str | None=None, observacoes: str | None=None) -> 'Investigacao':
        return cls(id=uuid4(), codigo_investigacao=codigo_investigacao.strip(), ocorrencia_id=ocorrencia_id, unidade_id=unidade_id, data_abertura=date.today(), status=StatusInvestigacao.ABERTA, delegado_responsavel_id=delegado_responsavel_id, data_conclusao=None, resumo=resumo.strip() if resumo else None, observacoes=observacoes.strip() if observacoes else None, ativo=True)

    def atualizar_status(self, status: StatusInvestigacao, observacoes: str | None=None) -> None:
        self.status = status
        if status in {StatusInvestigacao.CONCLUIDA, StatusInvestigacao.ARQUIVADA, StatusInvestigacao.REMETIDA_JUSTICA}:
            self.data_conclusao = date.today()
        self.ativo = status in {StatusInvestigacao.ABERTA, StatusInvestigacao.EM_ANDAMENTO}
        if observacoes:
            self.observacoes = observacoes.strip()