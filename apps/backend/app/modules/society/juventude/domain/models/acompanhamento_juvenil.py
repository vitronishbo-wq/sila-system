from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from uuid import UUID, uuid4
from app.modules.society.juventude.domain.enums import StatusAcompanhamento

@dataclass
class AcompanhamentoJuvenil:
    id: UUID
    codigo_acompanhamento: str
    jovem_id: UUID
    responsavel: str
    objetivo: str
    data_inicio: date
    data_registo: date
    status: StatusAcompanhamento = StatusAcompanhamento.ABERTO
    proxima_revisao: date | None = None
    historico: list[dict] | None = None
    observacoes: str | None = None
    ativo: bool = True

    @classmethod
    def abrir(cls, *, codigo_acompanhamento: str, jovem_id: UUID, responsavel: str, objetivo: str, data_inicio: date, proxima_revisao: date | None=None, observacoes: str | None=None) -> 'AcompanhamentoJuvenil':
        if len(responsavel.strip()) < 3:
            raise ValueError('Responsavel do acompanhamento deve ter pelo menos 3 caracteres')
        if len(objetivo.strip()) < 3:
            raise ValueError('Objetivo do acompanhamento deve ter pelo menos 3 caracteres')
        if proxima_revisao is not None and proxima_revisao < data_inicio:
            raise ValueError('Proxima revisao deve ser maior ou igual a data de inicio')
        return cls(id=uuid4(), codigo_acompanhamento=codigo_acompanhamento.strip(), jovem_id=jovem_id, responsavel=responsavel.strip(), objetivo=objetivo.strip(), data_inicio=data_inicio, data_registo=date.today(), proxima_revisao=proxima_revisao, observacoes=observacoes.strip() if observacoes else None, status=StatusAcompanhamento.ABERTO, ativo=True)

    def registrar_evolucao(self, descricao: str, proxima_revisao: date | None=None) -> None:
        if len(descricao.strip()) < 3:
            raise ValueError('Descricao da evolucao deve ter pelo menos 3 caracteres')
        if self.historico is None:
            self.historico = []
        self.historico.append({'data': date.today().isoformat(), 'descricao': descricao.strip()})
        if proxima_revisao is not None:
            self.proxima_revisao = proxima_revisao
        self.status = StatusAcompanhamento.EM_CURSO

    def encerrar(self, observacoes: str | None=None) -> None:
        self.status = StatusAcompanhamento.ENCERRADO
        self.ativo = False
        if observacoes is not None:
            self.observacoes = observacoes.strip() or None