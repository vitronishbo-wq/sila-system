from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from uuid import UUID, uuid4
from apps.backend.app.modules.society.juventude.domain.enums import StatusAcompanhamento, TipoSaudeJuvenil

@dataclass
class SaudeJuvenil:
    id: UUID
    codigo_registo: str
    jovem_id: UUID
    tipo_registo: TipoSaudeJuvenil
    descricao: str
    data_registo: date
    data_cadastro: date
    status_acompanhamento: StatusAcompanhamento = StatusAcompanhamento.ABERTO
    encaminhamento_necessario: bool = False
    observacoes: str | None = None
    ativo: bool = True

    @classmethod
    def registrar(cls, *, codigo_registo: str, jovem_id: UUID, tipo_registo: TipoSaudeJuvenil, descricao: str, data_registo: date, encaminhamento_necessario: bool=False, observacoes: str | None=None) -> 'SaudeJuvenil':
        if len(descricao.strip()) < 3:
            raise ValueError('Descricao do registo de saude deve ter pelo menos 3 caracteres')
        return cls(id=uuid4(), codigo_registo=codigo_registo.strip(), jovem_id=jovem_id, tipo_registo=tipo_registo, descricao=descricao.strip(), data_registo=data_registo, data_cadastro=date.today(), status_acompanhamento=StatusAcompanhamento.ABERTO, encaminhamento_necessario=encaminhamento_necessario, observacoes=observacoes.strip() if observacoes else None, ativo=True)

    def atualizar_acompanhamento(self, status: StatusAcompanhamento) -> None:
        self.status_acompanhamento = status
        self.ativo = status not in {StatusAcompanhamento.ENCERRADO, StatusAcompanhamento.SUSPENSO}