from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from uuid import UUID, uuid4

from apps.backend.app.modules.resources.ambiente.domain.enums import StatusFiscalizacao


@dataclass
class Fiscalizacao:
    id: UUID
    numero_fiscalizacao: str
    numero_licenca: str
    localidade: str
    objetivo: str
    fiscal_responsavel: str
    status: StatusFiscalizacao
    data_agendada: date
    data_realizacao: date | None = None
    relatorio: str | None = None
    observacoes: str | None = None

    @classmethod
    def agendar(
        cls,
        *,
        numero_licenca: str,
        localidade: str,
        objetivo: str,
        fiscal_responsavel: str,
        data_agendada: date,
    ) -> Fiscalizacao:
        if not localidade.strip():
            raise ValueError("Localidade da fiscalizacao e obrigatoria")
        if not objetivo.strip():
            raise ValueError("Objetivo da fiscalizacao e obrigatorio")
        if not fiscal_responsavel.strip():
            raise ValueError("Fiscal responsavel e obrigatorio")
        return cls(
            id=uuid4(),
            numero_fiscalizacao="",
            numero_licenca=numero_licenca,
            localidade=localidade.strip(),
            objetivo=objetivo.strip(),
            fiscal_responsavel=fiscal_responsavel.strip(),
            status=StatusFiscalizacao.AGENDADA,
            data_agendada=data_agendada,
        )

    def iniciar(self) -> None:
        if self.status != StatusFiscalizacao.AGENDADA:
            raise ValueError("Apenas fiscalizacao agendada pode ser iniciada")
        self.status = StatusFiscalizacao.EM_ANDAMENTO
        self.data_realizacao = date.today()

    def concluir(self, relatorio: str) -> None:
        if self.status != StatusFiscalizacao.EM_ANDAMENTO:
            raise ValueError("Fiscalizacao precisa estar em andamento para conclusao")
        if not relatorio.strip():
            raise ValueError("Relatorio de fiscalizacao e obrigatorio")
        self.status = StatusFiscalizacao.CONCLUIDA
        self.relatorio = relatorio.strip()
        if self.data_realizacao is None:
            self.data_realizacao = date.today()

    def cancelar(self, motivo: str) -> None:
        if self.status == StatusFiscalizacao.CONCLUIDA:
            raise ValueError("Fiscalizacao concluida nao pode ser cancelada")
        if self.status == StatusFiscalizacao.CANCELADA:
            raise ValueError("Fiscalizacao ja cancelada")
        if not motivo.strip():
            raise ValueError("Motivo do cancelamento e obrigatorio")
        self.status = StatusFiscalizacao.CANCELADA
        self.observacoes = motivo.strip()
