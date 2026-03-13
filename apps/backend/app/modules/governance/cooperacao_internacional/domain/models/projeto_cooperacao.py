from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date, datetime
from uuid import UUID, uuid4
from apps.backend.app.modules.governance.cooperacao_internacional.domain.enums import ModalidadeCooperacao, StatusProjeto, TipoProjeto

@dataclass
class ProjetoCooperacao:
    titulo: str
    tipo: TipoProjeto
    modalidade: ModalidadeCooperacao
    orgao_responsavel_id: UUID
    orgao_parceiro_id: UUID
    pais_parceiro_id: UUID
    data_inicio: date
    data_fim: date
    objetivo_geral: str
    objetivos_especificos: list[str]
    orcamento_total: float
    fonte_recursos: str
    acordo_base_id: UUID | None = None
    id: UUID = field(default_factory=uuid4)
    codigo_projeto: str = ''
    status: StatusProjeto = StatusProjeto.PROPOSTA
    atividades: list[dict] = field(default_factory=list)
    resultados: list[dict] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.codigo_projeto = self.codigo_projeto or self._gerar_codigo()
        if self.data_fim <= self.data_inicio:
            raise ValueError('Data fim deve ser maior que data inicio')
        if self.orcamento_total <= 0:
            raise ValueError('Orcamento total deve ser positivo')

    def _gerar_codigo(self) -> str:
        return f'COOP{datetime.utcnow().year}{uuid4().hex[:6].upper()}'

    def aprovar(self) -> None:
        self.status = StatusProjeto.APROVADO

    def iniciar_execucao(self) -> None:
        if self.status not in {StatusProjeto.APROVADO, StatusProjeto.EM_EXECUCAO}:
            raise ValueError('Projeto precisa estar aprovado para iniciar execucao')
        self.status = StatusProjeto.EM_EXECUCAO

    def concluir(self) -> None:
        self.status = StatusProjeto.CONCLUIDO

    def adicionar_atividade(self, *, descricao: str, data_prevista: date, responsavel: str, orcamento_previsto: float) -> None:
        self.atividades.append({'id': str(uuid4()), 'descricao': descricao, 'data_prevista': data_prevista.isoformat(), 'responsavel': responsavel, 'orcamento_previsto': orcamento_previsto, 'status': 'PENDENTE'})

    def registrar_atividade_concluida(self, *, atividade_id: str, data_realizacao: date, orcamento_realizado: float) -> None:
        for atividade in self.atividades:
            if atividade['id'] == atividade_id:
                atividade['status'] = 'CONCLUIDA'
                atividade['data_realizacao'] = data_realizacao.isoformat()
                atividade['orcamento_realizado'] = orcamento_realizado
                return
        raise ValueError('Atividade nao encontrada')

    def percentual_execucao(self) -> float:
        if not self.atividades:
            return 0.0
        concluidas = len([item for item in self.atividades if item.get('status') == 'CONCLUIDA'])
        return concluidas / len(self.atividades) * 100