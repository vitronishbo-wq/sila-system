from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID, uuid4
from apps.backend.app.modules.civil_protection.domain.enums import StatusDespacho

@dataclass
class Despacho:
    id: UUID
    codigo_despacho: str
    ocorrencia_id: UUID
    corporacao_id: UUID
    status: StatusDespacho
    data_despacho: datetime
    data_ultima_atualizacao: datetime
    bombeiro_responsavel_id: UUID | None = None
    meio_deslocamento: str | None = None
    observacoes: str | None = None
    ativo: bool = True

    @classmethod
    def gerar(cls, *, codigo_despacho: str, ocorrencia_id: UUID, corporacao_id: UUID, bombeiro_responsavel_id: UUID | None=None, meio_deslocamento: str | None=None, observacoes: str | None=None) -> 'Despacho':
        now = datetime.now()
        return cls(id=uuid4(), codigo_despacho=codigo_despacho.strip(), ocorrencia_id=ocorrencia_id, corporacao_id=corporacao_id, status=StatusDespacho.GERADO, data_despacho=now, data_ultima_atualizacao=now, bombeiro_responsavel_id=bombeiro_responsavel_id, meio_deslocamento=meio_deslocamento.strip() if meio_deslocamento else None, observacoes=observacoes.strip() if observacoes else None, ativo=True)

    def atualizar_status(self, status: StatusDespacho, observacoes: str | None=None) -> None:
        self.status = status
        self.data_ultima_atualizacao = datetime.now()
        self.ativo = status not in {StatusDespacho.CANCELADO}
        if observacoes:
            self.observacoes = observacoes.strip()