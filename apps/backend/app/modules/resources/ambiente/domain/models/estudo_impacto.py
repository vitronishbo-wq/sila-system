from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from uuid import UUID, uuid4
from apps.backend.app.modules.resources.ambiente.domain.enums import StatusEstudoAmbiental, TipoEstudoAmbiental

@dataclass
class EstudoImpacto:
    id: UUID
    numero_estudo: str
    numero_licenca: str
    tipo: TipoEstudoAmbiental
    descricao: str
    responsavel_tecnico: str
    status: StatusEstudoAmbiental
    data_submissao: date
    data_analise: date | None = None
    data_aprovacao: date | None = None
    analista_id: UUID | None = None
    observacoes: str | None = None

    @classmethod
    def submeter(cls, *, numero_licenca: str, tipo: TipoEstudoAmbiental, descricao: str, responsavel_tecnico: str) -> 'EstudoImpacto':
        if not descricao.strip():
            raise ValueError('Descricao do estudo e obrigatoria')
        if not responsavel_tecnico.strip():
            raise ValueError('Responsavel tecnico e obrigatorio')
        return cls(id=uuid4(), numero_estudo='', numero_licenca=numero_licenca, tipo=tipo, descricao=descricao.strip(), responsavel_tecnico=responsavel_tecnico.strip(), status=StatusEstudoAmbiental.SUBMETIDO, data_submissao=date.today())

    def iniciar_analise(self) -> None:
        if self.status not in {StatusEstudoAmbiental.SUBMETIDO, StatusEstudoAmbiental.COMPLEMENTACAO}:
            raise ValueError('Apenas estudo submetido ou em complementacao pode entrar em analise')
        self.status = StatusEstudoAmbiental.EM_ANALISE
        self.data_analise = date.today()

    def aprovar(self, analista_id: UUID) -> None:
        if self.status != StatusEstudoAmbiental.EM_ANALISE:
            raise ValueError('Estudo precisa estar em analise para aprovacao')
        self.status = StatusEstudoAmbiental.APROVADO
        self.data_aprovacao = date.today()
        self.analista_id = analista_id
        self.observacoes = None

    def solicitar_complementacao(self, analista_id: UUID, motivo: str) -> None:
        if self.status != StatusEstudoAmbiental.EM_ANALISE:
            raise ValueError('Estudo precisa estar em analise para solicitar complementacao')
        if not motivo.strip():
            raise ValueError('Motivo da complementacao e obrigatorio')
        self.status = StatusEstudoAmbiental.COMPLEMENTACAO
        self.analista_id = analista_id
        self.observacoes = motivo.strip()