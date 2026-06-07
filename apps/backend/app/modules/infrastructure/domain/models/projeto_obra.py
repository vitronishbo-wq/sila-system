from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from uuid import UUID, uuid4

from apps.backend.app.modules.infrastructure.domain.enums import StatusProjeto, TipoProjeto


@dataclass
class ProjetoObra:
    id: UUID
    codigo_projeto: str
    nome: str
    tipo: TipoProjeto
    status: StatusProjeto
    orgao_responsavel_id: UUID
    responsavel_tecnico_id: UUID
    valor_estimado: Decimal
    data_inicio_prevista: date
    data_fim_prevista: date
    data_cadastro: date
    obra_id: UUID | None = None
    descricao: str | None = None
    data_inicio_real: date | None = None
    data_fim_real: date | None = None
    versao: int = 1
    data_atualizacao: date | None = None
    observacoes: str | None = None

    @classmethod
    def criar(
        cls,
        *,
        codigo_projeto: str,
        nome: str,
        tipo: TipoProjeto,
        orgao_responsavel_id: UUID,
        responsavel_tecnico_id: UUID,
        valor_estimado: Decimal,
        data_inicio_prevista: date,
        data_fim_prevista: date,
        obra_id: UUID | None = None,
        descricao: str | None = None,
    ) -> ProjetoObra:
        if not codigo_projeto.strip():
            raise ValueError("Codigo do projeto e obrigatorio")
        if not nome.strip():
            raise ValueError("Nome do projeto e obrigatorio")
        if valor_estimado <= Decimal("0"):
            raise ValueError("Valor estimado deve ser maior que zero")
        if data_fim_prevista <= data_inicio_prevista:
            raise ValueError("Data fim prevista deve ser maior que data inicio prevista")
        return cls(
            id=uuid4(),
            codigo_projeto=codigo_projeto.strip(),
            nome=nome.strip(),
            tipo=tipo,
            status=StatusProjeto.ELABORACAO,
            orgao_responsavel_id=orgao_responsavel_id,
            responsavel_tecnico_id=responsavel_tecnico_id,
            valor_estimado=valor_estimado.quantize(Decimal("0.01")),
            data_inicio_prevista=data_inicio_prevista,
            data_fim_prevista=data_fim_prevista,
            obra_id=obra_id,
            descricao=descricao.strip() if descricao else None,
            data_cadastro=date.today(),
            versao=1,
        )

    def aprovar(self) -> None:
        if self.status != StatusProjeto.ELABORACAO:
            raise ValueError("Projeto precisa estar em elaboracao")
        self.status = StatusProjeto.APROVADO
        self.data_atualizacao = date.today()

    def iniciar_execucao(self, data_inicio: date) -> None:
        if self.status != StatusProjeto.APROVADO:
            raise ValueError("Projeto precisa estar aprovado")
        self.status = StatusProjeto.EM_EXECUCAO
        self.data_inicio_real = data_inicio
        self.data_atualizacao = date.today()

    def concluir(self, data_fim: date) -> None:
        if self.status != StatusProjeto.EM_EXECUCAO:
            raise ValueError("Projeto precisa estar em execucao")
        self.status = StatusProjeto.CONCLUIDO
        self.data_fim_real = data_fim
        self.data_atualizacao = date.today()

    def revisar(self, motivo: str) -> None:
        if self.status not in {StatusProjeto.APROVADO, StatusProjeto.EM_EXECUCAO}:
            raise ValueError("Projeto nao pode ser revisado neste status")
        if not motivo.strip():
            raise ValueError("Motivo da revisao e obrigatorio")
        self.status = StatusProjeto.ELABORACAO
        self.versao += 1
        self.observacoes = motivo.strip()
        self.data_atualizacao = date.today()

    def arquivar(self, motivo: str) -> None:
        if self.status == StatusProjeto.ARQUIVADO:
            raise ValueError("Projeto ja arquivado")
        if not motivo.strip():
            raise ValueError("Motivo do arquivamento e obrigatorio")
        self.status = StatusProjeto.ARQUIVADO
        self.observacoes = motivo.strip()
        self.data_atualizacao = date.today()
