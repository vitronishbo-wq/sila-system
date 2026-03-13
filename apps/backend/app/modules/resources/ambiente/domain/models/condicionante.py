from __future__ import annotations
from dataclasses import dataclass
from datetime import date, timedelta
from uuid import UUID, uuid4
from apps.backend.app.modules.resources.ambiente.domain.enums import StatusCondicionante

@dataclass
class Condicionante:
    id: UUID
    codigo_condicionante: str
    numero_licenca: str
    descricao: str
    prazo_dias: int
    status: StatusCondicionante
    data_criacao: date
    data_limite: date
    data_cumprimento: date | None = None
    evidencia: str | None = None
    observacoes: str | None = None

    @classmethod
    def criar(cls, *, numero_licenca: str, descricao: str, prazo_dias: int) -> 'Condicionante':
        if not descricao.strip():
            raise ValueError('Descricao da condicionante e obrigatoria')
        if prazo_dias <= 0:
            raise ValueError('Prazo da condicionante deve ser maior que zero')
        data_criacao = date.today()
        return cls(id=uuid4(), codigo_condicionante='', numero_licenca=numero_licenca, descricao=descricao.strip(), prazo_dias=prazo_dias, status=StatusCondicionante.PENDENTE, data_criacao=data_criacao, data_limite=data_criacao + timedelta(days=prazo_dias))

    def iniciar_cumprimento(self) -> None:
        if self.status != StatusCondicionante.PENDENTE:
            raise ValueError('Apenas condicionante pendente pode iniciar cumprimento')
        self.status = StatusCondicionante.EM_CUMPRIMENTO

    def registrar_cumprimento(self, evidencia: str | None=None) -> None:
        if self.status not in {StatusCondicionante.PENDENTE, StatusCondicionante.EM_CUMPRIMENTO}:
            raise ValueError('Condicionante nao pode ser marcada como cumprida neste status')
        self.status = StatusCondicionante.CUMPRIDA
        self.data_cumprimento = date.today()
        self.evidencia = evidencia

    def marcar_descumprimento(self, motivo: str) -> None:
        if not motivo.strip():
            raise ValueError('Motivo do descumprimento e obrigatorio')
        self.status = StatusCondicionante.DESCUMPRIDA
        self.observacoes = motivo.strip()